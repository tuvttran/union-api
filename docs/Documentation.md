# Union Board Documentation

## Table of contents:
* [Requests](#requests)
* [Progress](#progress)
* [API Endpoints](#api-endpoints)
* [Sample Data Format](#sample-data-format)
* [Database Design](#database-design)

## Requests:

Verb | Description
---------|----------
 GET | Used for retrieving resources.
 POST | Used for creating resources
 PUT | Used for changing/replacing resources
 DELETE | Used for deleting resources

## Progress:
- [x] `GET /companies`
- [x] `GET /companies/{company_id}`
- [ ] `GET /companies/{company_id}?fields={name,emails,website,bio}`
- [x] `GET /companies/{company_id}/{metric}`
- [x] `GET /metrics`
- [x] `POST /companies`
- [x] `POST /companies/{company_id}`
- [ ] `PUT /companies/{company_id}`
- [x] `PUT /companies/{company_id}/metrics`
- [x] `POST /auth/login`
- [x] `POST /auth/change`
- [x] `GET /auth/status`
- [x] `POST /auth/logout` (Implemented by frontend side)


## API Endpoints:

### Startup-related API:

 Method | Endpoint | Usage | Returns | Authentication
---------|----------|--------- | ---------- | ---------
 GET | `/companies` | Get all companies' information | Arrays of companies | Staff
 GET | `/companies/{company_id}` | Get a company information | Object including name, founders' email and bio | Staff and non-staff
 GET | `/companies/{company_id}?fields={name,emails,website,bio}` | Get a company information based on particular parameters | Object including fields specified in the request parameter | Staff and non-staff
 GET | `/companies/{company_id}/metrics` | Get a company's weekly metrics information | Company's name and sales | Staff and non-staff
 GET | `/metrics` | Get a list of all the metrics | an object containing a metric's name | Staff and non-staff
 POST | `/companies` | Create a new company | success/error message and company object | Staff
 POST | `/companies/{company_id}` | Add KPI metrics to a company | success/error message and the metrics recently added | Staff and non-staff
 PUT | `/companies/{company_id}` | Update a company's information (name, website, bio and founder) | success/error message and data recently updated | Staff and non-staff
 PUT | `/companies/{company_id}/metrics` | Update a company's metric (value and updated_at field) | success/error message and data recently updated | Staff and non-staff

### Authentication API:

 Method | Endpoint | Usage | Returns | Authentication
---------|----------|--------- | ---------- | ---------
 POST | `/auth/login` | Log in | status and authentication token | None
 POST | `/auth/change` | Change a user's password | status and message | OAuth
 GET | `/auth/status` | Check the current status of the user, whether Brandery staff or startup founders | object with user information | OAuth
 POST | `/auth/logout` | Log out | status and message | OAuth

## Sample Data Format:

### Authorization:

```http
Authorization: Bearer {{auth_token}}
```

### `GET /companies`

#### Return format:
```json
{
    "total": 2,
    "companies": {
        "Demo": {
            "id": 145,
            "founders": [
                {
                    "name": "Tu Tran",
                    "email": "tu@demo.com",
                    "role": "CTO"
                },
                {
                    "name": "John Average",
                    "email": "john@demo.com",
                    "role": "CEO"
                }
            ],
            "website": "http://www.demo.com",
            "bio": "This is a demo company. Nothing too special here."
        },
        "Boocoo": {
            "id": 2030,
            "founders": [
                {
                    "name": "Jane Jacob",
                    "email": "jane@boocoo.club",
                    "role": "CEO"
                }
            ],
            "website": "http://boocoo.club",
            "bio": "Boocoo is a AI startup specializing in random stuff."
        }
    }
}
```

### `GET /companies/{company_id}`

#### Return format:
```json
{
    "id": 145,
    "name": "Demo",
    "website": "http://demo.com",
    "founders" : [
        {
            "name": "Tu Tran",
            "email": "tu@demo.com",
            "role": "CTO"
        },
        {
            "name": "John Average",
            "email": "john@demo.com",
            "role": "CEO"
        }
    ],
    "bio": "This is a demo company. Nothing too special here"
}
```

### `GET /companies/{company_id}/metrics`

#### Return format:
```json
{
    "sales": {
        "weeks": 4,
        // "%a, %d %b %Y %H:%M:%S GMT"
        "last_updated": "Fri, 16 Jun 2017 15:57:23 GMT",
        "data": [12, 34, 56, 23]
    },
    "traffic": {
        // same as above
    },
    "subscribers": {
        // same as above
    },
    "active_users": {
        // same as above
    },
    "paying_users": {
        // same as above
    },
    "engagement": {
        // same as above
    },
    "mrr": {
        // same as above
    },
    "cpa": {
        // same as above
    },
    "pilots": {
        // same as above
    },
    "product_releases": {
        // same as above
    },
    "preorders": {
        // same as above
    },
    "automation_percents": {
        // same as above
    },
    "conversion_rate": {
        // same as above
    },
    "marketing_spent": {
        // same as above
    },
    "other_1": {
        // same as above
    },
    "other_2": {
        // same as above
    }
}
```

### `GET /metrics`

#### Return format:
```json
{
    "active_users": {
        "name": "Active users"
    },
    "automation_percents": {
        "name": "Percents of automation"
    },
    "conversion_rate": {
        "name": "Conversion rate"
    },
    "cpa": {
        "name": "Cost per acquisition"
    },
    "engagement": {
        "name": "Engagement"
    },
    "marketing_spent": {
        "name": "Marketing spent"
    },
    "mrr": {
        "name": "Revenue"
    },
    "other_1": {
        "name": "Other metric 1"
    },
    "other_2": {
        "name": "Other metric 2"
    },
    "paying_users": {
        "name": "Paying users"
    },
    "pilots": {
        "name": "Pilots"
    },
    "preorders": {
        "name": "Preorders"
    },
    "product_releases": {
        "name": "Product releases"
    },
    "sales": {
        "name": "Sales"
    },
    "subscribers": {
        "name": "Subscribers"
    },
    "traffic": {
        "name": "Traffic"
    }
}
```

### `POST /companies`

#### Request body:
```json
{
    "name": "Demo",
    "founders": [
        {
            "name": "Tu Tran",
            "email": "tu@demo.com",
            "role": "CTO"
        },
        {
            "name": "John Average",
            "email": "john@demo.com",
            "role": "CEO"
        }
    ],
    "website": "http://www.demo.com",
    "bio": "This is a demo company. Nothing too special here."
}
```

#### Return format:
On success:
```json
{
    "status": "success",
    "message": "new company created!",
    "id": 12342345
}
```

On failure:
```json
{
    "status": "failure",
    "message": "error message"
}
```

### `POST /companies/{company_id}`

#### Request body:
```json
{
    "sales": 123.7,
    "traffic": 950,
    "subscribers": 500,
    "active_users": 500,
    "paying_users": 23,
    "engagement": 500,
    "mrr": 500,
    "cpa": 500,
    "pilots": 500,
    "product_releases": 500,
    "preorders": 500,
    "automation_percents": 500,
    "conversion_rate": 500,
    "marketing_spent": 500,
    "other_1": 500,
    "other_2": 500
}
```
**Note**: Any fields can be omitted but **cannot** be empty

#### Return format:
On success:
```json
{
    "status": "success",
    "message": "metrics added",
    "metrics_added": {
        "sales": 123.7,
        "traffic": 950,
        "subscribers": 500,
        "active_users": 500,
        "paying_users": 23,
        "engagement": 500,
        "mrr": 500,
        "cpa": 500,
        "pilots": 500,
        "product_releases": 500,
        "preorders": 500,
        "automation_percents": 500,
        "conversion_rate": 500,
        "marketing_spent": 500,
        "other_1": 500,
        "other_2": 500
    }
}
```

On failure:
```json
{
    "status": "failure",
    "message": "one of the metrics is empty"
}
```

### `POST /auth/login`

#### Request Body:
```json
{
    "email": "john.doe@companyx.com",
    "password": "123456"
}
```

#### Return format:
On success:
```json
{
    "status": "success",
    "message": "logged in",
    "auth_token": "AaDEW143G@d"
}
```

On failure:
```json
{
    "status": "failure",
    "message": "wrong password or user does not exist"
}
```

### `POST /auth/change`

#### Request body:
```json
{
    "new_email": "john.average@example.com",
    "old_password": "thisisold",
    "new_password": "thisisnew",
}
```

#### Return format:

On success:
```json
{
    "status": "success",
    "message": "successfully changed password"
}
```

On failure:
```json
{
    "status": "failure",
    "message": "old password is incorrect
}
```

### `GET /auth/status`

#### Return format:
On success:
```json
{
    "status": "success",
    "data": {
        "user_id": 12,
        "email": "staff@brandery.org",
        "company": "The Brandery",
        "registered_on": "Tue, Jun 20 2017",
        "staff": true
    }
}
```

On failure:
```json
{
    "status": "failure",
    "message": "unauthorized"
}
```

## Database Design:

### Company:
```yaml
- id:           integer
- name:         string
- founders:     array
- website:      string
- bio:          text
```

### Founder
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- email:        string
- name:         string
- role:         string
```

### User
```yaml
- id:           integer
- founder_id:   integer # Foreign Key to Founder table
- email:        integer
- password:     string
- created_at:   datetime
- staff:        boolean
```

### Metric:
Type of metrics:
 - ActiveUser
 - PayingUser
 - Subscriber
 - Engagement
 - MRR (monthly recurring revenue)
 - Sale
 - Pilot
 - Traffic
 - ProductRelease
 - Preorder
 - AutomationPercentage
 - CPA (cost per acquisition)
 - ConversionRate
 - MarketingSpent
 - Other1
 - Other2
```yaml
- id:           integer
- company_id:   integer  # Foreign Key to Company table
- week:         integer
- updated_at:   datetime
- value:        double
```

### Note (NoSQL database)
```json
{
    "user_id": {
        "table_name": "notes"
    }
}
```
