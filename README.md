## WooCommerce Django Integration
This small example tries to show how to consume WooCommerce rest API, by setting up customers

###Prerequisites
- Please go through this [documentation](https://woocommerce.github.io/woocommerce-rest-api-docs/?python#introduction) first
- Set up a Wordpress server and install WooCommerce.
- Create API Keys and set the following values in your env variables 
    * WOO_CONSUMER_KEY - with the value of the consumer key
    * WOO_CONSUMER_SECRET - with the value of the consumer secret
- Install docker

### Running the app
- clone the project
- `cd` into the project folder
- run `docker-compose up` once the docker container are up navigate to `http://localhost:8009/`
- Register an account
- Login using the credentials that you have registered with and have fun coding

### Known Issues
- The delete functionality keeps returning the error `'true? is not of type boolean.'`
this means the delete functionality is not working as expected.