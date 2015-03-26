Supermarket checkout project

Author: Beth Ginsberg

-----------------------------------

I was posed the following question to complete as homework:

  Step 1: Shopping cart
  You are building a checkout system for a shop which only sells apples and oranges. 
  Apples cost 60p and oranges cost 25p.
  Build a checkout system which takes a list of items scanned at the counter and outputs the total cost
  For example: [ Apple, Apple, Orange, Apple ] => $2.05
  Make reasonable assumptions about the inputs to your solution; for example, many candidates take a list of strings as input

  Step 2: Simple offers
  The shop decides to introduce two new offers
  buy one, get one free on Apples
  3 for the price of 2 on Oranges
  Update your checkout functions accordingly.

  You can write this as a simple REST service if you wish using your language and framework of choice, you can mock up parts if you wish to.
  Please, include tests and documentation. Please, use git to check in your code for step 1. and step2. as separate commits/pushes.
  Looking for approach to development, design patterns, code readability, comments, tests and error handling, documentation.

This repository contains my solution to both steps. Step 1 is completed in the following commit:
https://github.com/bhg/supermarket/commit/aeac1b690206dc3267698e056eac9936a0084df2

Step 2 is completed in the following commit:

-----------------------------------

To test this code, you will need the following prerequisites:
 - python
 - django
 - a browser, curl or a similar tool

Once you have these, perform the following steps:

 $ git clone https://github.com/bhg/supermarket
 $ cd supermarket
 $ python manage.py test

Since I have generalised the solution to allow for any products or discounts, the specific question can be answered by populating the database with the input data in question. This can be done as follows:

 For Step 1:
 $ python manage.py dbshell
 sqlite> insert into checkout_product values ('apple', 0.6, null, null);
 sqlite> insert into checkout_product values ('orange', 0.25, null, null); 

 For Step 2 (either delete the values from Step 1 or perform an update):
 sqlite> insert into checkout_product values ('apple', 0.6, 1, 2);
 sqlite> insert into checkout_product values ('orange', 0.25, 2, 3);

To check the results:
 $ python manage.py runserver

In a browser navigate to http://127.0.0.1:8000/purchase/
Login with username "admin" and password "admin"
In the "Items list" field, type the list of items in the purchase. Click "POST" and the resulting total should appear.

This may also be done using curl or a similar tool.
