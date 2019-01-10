# Britecore Insurance Web Service
*Not just homes, farms and churches!*
[![Build Status](https://travis-ci.org/andrew-snek/project-x.svg?branch=master)](https://travis-ci.org/andrew-snek/project-x)
[![codecov](https://codecov.io/gh/andrew-snek/project-x/branch/master/graph/badge.svg)](https://codecov.io/gh/andrew-snek/project-x)
## Intro
BIWS is a risk management system which allows to manage different kinds of risks. You can create *Field Types* with various widgets and validation rules, arrange them into collections called *Abstract Risks*, which you can then populate with data.

The project is built using **Django + DRF** for a backend - deployed to **AWS Lambda** using **Zappa**, and **VueJS** SPA for a frontend - deployed to an **S3** bucket and served by **CloudFront**. Both these parts(as well as **PostgreSQL** database and **Selenium** standalone testing server) are **docker**ized, and application is deployed automatically by the continuous integration service **Travis-CI** every time there is a push to master with passing tests.

So, it's just "docker-compose up" to build and run with hot reload on code change, and then just "git push" to deploy. Ain't this it, chief?

**Currently deployed instance**, login with *admin:admin*: https://d6aht25yrtwu9.cloudfront.net

![Risk creation UI](https://user-images.githubusercontent.com/45121397/50987101-4bb08e00-1511-11e9-9923-0b166302a576.png)


## Tech stack, detailed:
### Database
- **PostgreSQL 10** both locally and as an engine for AWS RDS. But we use only a basic subset of SQL here(, except maybe transactions with the strictest isolation level), so technically any relational DB except MySQL(with MyISAM) will do.

**A note on data model**. Distilled to its pure metaphysical essence, our app just needs to allow users to create and fill in different forms. How hard can that be? Turns out, for relational databases - quite. There are roughly three ways to make it work, though: Entity-Attribute-Value pattern, storing data in JSON(or XML, if using MS SQL) fields, or changing schema dynamically. Long story short: EAV is easiest to maintain, but slowest to perform; "changing schema" is fastest to perform, but hardest to maintain; and "data in JSON/XML" is in the middle on both counts. So in the long run I would advise to start with flexible EAV and after stabilization of features to move towards faster patterns, if performance becomes a problem.

Here is the diagram of our database, with tables structured according to EAV:
![Data Model](https://user-images.githubusercontent.com/45121397/50982309-91675980-1505-11e9-8acf-8fa8c23ce3a2.png)



### Backend
  - based on **Django 2** and **Django Rest Framework 3.7**;
  - compliant with **flake8**, **"Two Scoops"*** and talks of Raymond Hattinger;
  - tested with **py.test**;
  - environment variables are passed through **python-decouple**;
  - packages are counted by **pipenv**;
  - user control done by **djangorestframework-simplejwt**.

**A note on tests**. I'll start from a distance, please bear with me. What is a better way to write a file with our project's requirements - simple and readable, only top-level dependencies, or every dependency with its version exactly, like a "pip freeze" would generate? The second approach seems to be the way to go if we are forced to choose, but it's just cumbersome. Can we do better? Yes, we can have the best of both worlds - two files. And we don't need to do it by hand, Kenneth Reitz has already wrote [a tool for that](https://www.kennethreitz.org/essays/a-better-pip-workflow).

Now a similar question about tests. What's better - to have quick, mocked, in-memory suite of unit tests, or slow, integrated, end-to-end test suite with real services? Obviously, the same test cannot be fast while using real services, yet we want both. The answer? Two test suites: one fast and mocked, other slow and real, each covering the code 100%. There is a name for this style of testing - [London School of TDD](https://github.com/testdouble/contributing-tests/wiki/London-school-TDD), and that's how tests for this project are written. One nice consequence of this approach is that we don't have to write integration tests, from the middle of the [testing pyramid](https://github.com/testdouble/contributing-tests/wiki/Testing-Pyramid).

* The only exception is public exposure of serial primary keys.

### Frontend
- a single page application using **VueJS** together with **Vue Router** and **Vuex**;
- beautified with **Vuetify** - Material Design CSS framework - aka "that google buttons styling thing";
- networking is taken care of by **axios**;
- **ESLint, Babel and Webpack** do their things;
- users are identified by **JSON Web Tokens**, which are refreshed automatically using the hippest Javascript feature called **setTimeout**.

Tests here are only "smoke" ones, pre-generated by vue-cli. But I integrated them into the continuous delivery pipeline(**Selenium** is here specifically for this) and deliberately chose **Jest + Nightwatch** as runners, so they are ready to be written.

### Deployment
Both frontend and backend live in the same repo for simplicity, but in different **Docker** images. Backend uses **lambdaci/build-python3.6**, which imitates AWS Lambda environment (It is also possible to run our code in a "real Lambda" mode using "run" image lambdaci/python3.6, but I didn't find that useful.), while front is on minimalist **mhart/alpine-node**. During the build phase the code is not copied into images, but mounted into the running containers by compose, making hot reload possible.

So workflow goes like this: clone the repo, create new branch, "docker-compose up" to see it running, write tests, run them in containers, see them fail, write some code, see code work after the hot reload, run tests again to see them pass, commit, merge into master(with rebase and --no-ff, preferably), push and see **Travis** building the images, testing the code and deploying it to Lambda and **S3/CloudFront**.

That's the workflow for updating the already existing deployment, though. Initial rollout is a bit more involved. You would need to:
1. Create an Amazon RDS.
2. Using db's endpoint from Step 1, initiate Zappa deployment
3. Using Lambda's endpoint from Step 2, build production version of Vue frontend and upload it to S3 bucket, connected with CloudFront.

**Important**: initiating and updating Zappa deployment, as well as building and uploading Vue frontend, should be done exclusively in Docker containers. See .travis.yml file how continuous integration system is set to do it, for inspiration.

Ideally you would initially deploy the whole thing just by creating a CloudFormation stack, and one day I will know how to integrate Zappa into that thing.

### References:
*Data Model*

See presentation by Juergen Schackmann at DjangoCon EU 2013: Dynamic Models in Django, comparing different approaches to implementing dynamic models

video: https://www.youtube.com/watch?v=67wcGdk4aCc

slides: https://www.slideshare.net/schacki/django-dynamic-models20130502

Many people strongly condemn Entity-Attribute-Value, calling it an anti-pattern:
- D. Fontaine, "Mastering PostgreSQL", 6.5 Modelization Anti-Patterns;
- B. Karwin, "SQL Antipatterns", Logical Database Design Antipatterns, Entity-Attribute-Value;

so we should start thinking as early as possible about moving from it.

*Backend*

Some extremely good talks that explain and justify the testing approach I use here
- [Please don’t mock me (and other test double advice)](https://vimeo.com/257056050) by Justin Searls
- [Integrated Tests Are A Scam](https://vimeo.com/80533536) by J.B. Rainsberger
