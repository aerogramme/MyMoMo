# MyMoMo.io
```
Simple Mobile Money Wallet Application 
```

# Features
```
- Users can Top Up money on their mobile money wallet
- Users can Transfer money to other mobile money wallet
- Users can Withdraw money from their mobile money wallet
```

# Installation & Requirements
- Python 3
- Python Flask Micro-framework
- Docker
- MongoDB
   - Create the following collections:
	  - Topup
	  - Transfer
	  - Withdrawal

# Running the app in docker container

##### Using Docker:
```
- docker-compose up
```
##### CD into Docker container
```
- docker-compose exec -it <name of container> bash
```

# Running the app locally

```
python app.py
```
# API EndPoints
##### POST Request:
```
EndPoints:
 - https://kubedoc.appspot.com/momo/api/v1/addcash
 - https://kubedoc.appspot.com/momo/api/v1/withdraw
 - https://kubedoc.appspot.com/momo/api/v1/transfer
 - https://kubedoc.appspot.com/momo/api/v1/balance/<<string:phone>>
 - https://kubedoc.appspot.com/momo/api/v1/get-transaction-status/<<string:transaction_id>>
 - https://kubedoc.appspot.com/momo/api/v1/account-verification/<<string:phone>>

Host : https://kubedoc.appspot.com
Authorization: Basic {ACCESS_TOKEN}
Content-Type: application/json
Basic Auth ->  "username": "freeworldboss", "password": "cq#4&Ds6~K+0iwU_"

```
 - Body
 
| Field      | Required   |         Type          |
|------------|------------|-----------------------|
| FirstName  | False      | String                |
| LastName   | False      | String                |
| fromPhone  | True       | String eg. 0243559227 |
| toPhone    | True       | String                |
| email      | False      | String                |
| amount     | True       | Float  eg. 8749.31    |
| description| False      | String                |
| service_type| False     | String eg. Wallet     |

    ```
     {
       "firstname":"THEOPHILUS",
       "lastname":"SIAMEH",
       "fromPhone":"0243559227",
       "toPhone":"0205592278",
       "email":"theodondre@gmail.com",
       "amount": 8749.31,
       "service_type":"Wallet",
       "description":"Testing transaction"
    }
    ```


#### GET Request:

```bash
GET transaction status

        -  http://127.0.0.1:5000/momo/api/v1/get-transaction-status/<<string:transaction_id>>

        -  https://kubedoc.appspot.com/momo/api/v1/get-transaction-status/0089fc37-0aa0-485a-b40d-ffc67d347c1a

GET account verification:

        -  http://127.0.0.1:5000/momo/api/v1/account-verification/<<string:phone>>

        -  https://kubedoc.appspot.com/momo/api/v1/account-verification/0243559227

```

```bash
curl -X GET http://127.0.0.1:5000/momo/api/v1/get-transaction-status/0089fc37-0aa0-485a-b40d-ffc67d347c1a

curl -X GET https://kubedoc.appspot.com/momo/api/v1/get-transaction-status/0089fc37-0aa0-485a-b40d-ffc67d347c1a

Response:
      ```
        {
          "code": 200,
          "response": {
            "Amount": 40.0,
            "ConfirmationNumber": "TNF-20200316-D10197",
            "Created_At": "2020-03-16 17:46:36",
            "Phone": "0205592278",
            "TransactionID": "0089fc37-0aa0-485a-b40d-ffc67d347c1a"
          },
          "status": "SUCCESS"
        }
       ```
curl -X GET https://kubedoc.appspot.com/momo/api/v1/balance/0243559227

Response:
      ```
        {
          "code": 200,
          "response": {
            "registered_name": "THEOPHILUS SIAMEH",
            "registration_status": "Registered"
          },
          "status": "SUCCESS"
        }
        ```
```


# TopUp POST request
 ![alt text](https://github.com/aerogramme/mymomo/blob/master/addcash.png)

# Transfer POST request
 ![alt text](https://github.com/aerogramme/mymomo/blob/master/transfer.png)

# CURL

```
Localhost:

curl -X POST \
  http://127.0.0.1:5000/momo/api/v1/transfer/ \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Basic ZnJlZXdvcmxkYm9zczpjcSM0JkRzNn5LKzBpd1Vf' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 307' \
  -H 'Content-Type: application/json' \
  -H 'Host: 127.0.0.1:5000' \
  -H 'cache-control: no-cache' \
  -d '{
   "firstname":"THEOPHILUS",
   "lastname":"SIAMEH",
   "fromPhone":"0243559227",
   "toPhone":"0205592278",
   "email":"theodondre@gmail.com",
   "amount": 8749.31
}'

Response:
```
    {
      "amount": 530.0,
      "code": 200,
      "confirmation_Number": "TNF-20200317-903AAB",
      "message": "Money transferred successfully from your wallet",
      "status": "SUCCESS",
      "transaction_ID": "ff62e746-0d99-40ab-bd33-6a62ddf2d522"
    }
```


Remote:

 curl -X POST \
  http://35.245.216.6:80/momo/api/v1/addcash/ \
  -H 'Accept: */*' \
  -H 'Authorization: Basic ZnJlZXdvcmxkYm9zczpjcSM0JkRzNn5LKzBpd1Vf' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 233' \
  -H 'Content-Type: application/json' \
  -H 'Host: 35.236.211.103:80' \
  -H 'User-Agent: PostmanRuntime/7.18.0' \
  -H 'cache-control: no-cache' \
  -d '{
   "firstname":"THEOPHILUS",
   "lastname":"SIAMEH",
   "fromPhone":"0243559227",
   "toPhone":"0205592278",
   "email":"theodondre@gmail.com",
   "amount": 8749.31
}'

Response:
```
    {
      "amount": 345.0,
      "code": 200,
      "confirmation_Number": "ADC-20200317-D3976D",
      "message": "Money added successfully to your wallet",
      "response": "Transaction was successful",
      "status": "SUCCESS",
      "transaction_ID": "6f647175-48f0-4368-b77d-bc7aa6979b38"
    }
```
```
# PYTHON
```
import requests

url = "http://35.245.216.6:80/momo/api/v1/balance/"

payload = "{"firstname\":\"THEOPHILUS\",\n   \"lastname\":\"SIAMEH\",\n   \"fromPhone\":\"0243559227\",\n   \"toPhone\":\"0205592278\",\n   \"email\":\"theodondre@gmail.com\",\n   \"amount\": 8749.31}"

headers = {
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "35.236.211.103:80",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "233",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
```

# JAVA
```
public final String BASE_URL = "http://35.245.216.6:80/momo/api/v1/balance/"
OkHttpClient client = new OkHttpClient();

MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType,
    "{\"firstname\":\"THEOPHILUS\",\n
      \"lastname\":\"SIAMEH\",\n
      \"fromPhone\":\"0243559227\",\n
      \"toPhone\":\"0205592278\",\n
      \"email\":\"theodondre@gmail.com\",\n
      \"amount\": 8749.31,\n
    }");

Request request = new Request.Builder()
  .url(BASE_URL)
  .post(body)
  .addHeader("Content-Type", "application/json")
  .addHeader("Accept", "*/*")
  .addHeader("Cache-Control", "no-cache")
  .addHeader("Host", "35.236.211.103:80")
  .addHeader("Accept-Encoding", "gzip, deflate")
  .addHeader("Content-Length", "233")
  .addHeader("Connection", "keep-alive")
  .addHeader("cache-control", "no-cache")
  .build();

Response response = client.newCall(request).execute();
```

# PHP
```
<?php <br/>
$request = new HttpRequest();
$request->setUrl('http://35.245.216.6:80/momo/api/v1/balance/');
$request->setMethod(HTTP_METH_POST);

$request->setHeaders(array(
  'cache-control' => 'no-cache',
  'Connection' => 'keep-alive',
  'Content-Length' => '233',
  'Accept-Encoding' => 'gzip, deflate',
  'Host' => '35.236.211.103:80',
  'Cache-Control' => 'no-cache',
  'Accept' => '*/*',
  'User-Agent' => 'PostmanRuntime/7.18.0',
  'Content-Type' => 'application/json'
));

$request->setBody('{
   "firstname":"THEOPHILUS",
   "lastname":"SIAMEH",
   "fromPhone":"0243559227",
   "toPhone":"0205592278",
   "email":"theodondre@gmail.com",
   "amount": 8749.31
}');

try {
  $response = $request->send();
  echo $response->getBody();
} catch (HttpException $ex) {
  echo $ex;
}
```


# LICENSE
```
	Copyright (C) 2020 https://mymomo.io

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	https://github.com/aerogramme/momo/LICENSE

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
```

# CONTACT US
```
 	- Please, contact us via support@mymomo.io if you are using this library, just to let us know :) Thank you! <br/>
```
# CONTRIBUTORS
```
 	- THEOPHILUS SIAMEH | @tsiameh
        - EMMANUEL AKRASHIE
 ```
