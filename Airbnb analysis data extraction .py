
# In[1]:


import pymongo
import pandas as pd
from pymongo import MongoClient
pd.set_option('display.max_columns', None)


# In[2]:


cloud_client = MongoClient("mongodb+srv://kiruthickagp:LjXSFf3v8QMoZut8@cluster0.87vfp8s.mongodb.net/?retryWrites=true&w=majority")


# In[3]:


db = cloud_client["sample_airbnb"]


# In[4]:


col= db["listingsAndReviews"] 


# In[5]:


data = []
for i in col.find( {}, {'_id': 1, 'name': 1, 'host_id': 1, 'host_name': 1, 'neighbourhood_group': 1, 'neighbourhood': 1,
                        'latitude': 1, 'longitude': 1, 'room_type': 1, 'price': 1, 'minimum_nights': 1, 'number_of_reviews': 1,
                        'last_review': 1, 'reviews_per_month': 1, 'calculated_host_listings_count': 1, 'availability_365': 1,
                        'property_type': 1, 'room_type': 1, 'bed_type': 1,
                        'minimum_nights': 1, 'maximum_nights': 1, 'cancellation_policy': 1, 'accommodates': 1,
                        'bedrooms': 1, 'beds': 1, 'number_of_reviews': 1, 'bathrooms': 1, 'price': 1,
                        'cleaning_fee': 1, 'extra_people': 1, 'guests_included': 1, 'images.picture_url': 1,
                        'review_scores.review_scores_rating': 1} ):
    data.append(i)

df_1 = pd.DataFrame(data)
df_1['images'] = df_1['images'].apply(lambda x: x['picture_url'])
df_1['review_scores'] = df_1['review_scores'].apply(lambda x: x.get('review_scores_rating', 0))
df_1.head()


# In[6]:


df_1


# In[7]:


df_1.isnull().sum()


# In[8]:


df_1['bedrooms'].fillna(0, inplace=True)
df_1['beds'].fillna(0, inplace=True)
df_1['bathrooms'].fillna(0, inplace=True)
df_1['cleaning_fee'].fillna('Not Specified', inplace=True)
df_1.isnull().sum()


# In[9]:


df_1.dtypes


# In[10]:


df_1['minimum_nights'] = df_1['minimum_nights'].astype(int)
df_1['maximum_nights'] = df_1['maximum_nights'].astype(int)
df_1['bedrooms'] = df_1['bedrooms'].astype(int)
df_1['beds'] = df_1['beds'].astype(int)
df_1['bathrooms'] = df_1['bathrooms'].astype(str).astype(float)
df_1['price'] = df_1['price'].astype(str).astype(float).astype(int)
df_1['cleaning_fee'] = df_1['cleaning_fee'].apply(lambda x: int(float(str(x))) if x != 'Not Specified' else 'Not Specified')
df_1['extra_people'] = df_1['extra_people'].astype(str).astype(float).astype(int)
df_1['guests_included'] = df_1['guests_included'].astype(str).astype(int)
     


# In[11]:


df_1.dtypes


# In[12]:


df_1.describe().T


# In[13]:


df_1.head(2)


# In[14]:


host = []
for i in col.find( {}, {'_id':1, 'host':1}):
    host.append(i)

df_host = pd.DataFrame(host)
host_keys = list(df_host.iloc[0,1].keys())
host_keys.remove('host_about')

for i in host_keys:
    if i == 'host_response_time':
        df_host['host_response_time'] = df_host['host'].apply(lambda x: x['host_response_time'] if 'host_response_time' in x else 'Not Specified')
    else:
        df_host[i] = df_host['host'].apply(lambda x: x[i] if i in x and x[i]!='' else 'Not Specified')

df_host.drop(columns=['host'], inplace=True)
df_host.head()


# In[15]:


df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False:'No',True:'Yes'})
df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False:'No',True:'Yes'})
df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False:'No',True:'Yes'})
df_host.head()
     


# In[16]:


df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False:'No',True:'Yes'})
df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False:'No',True:'Yes'})
df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False:'No',True:'Yes'})
df_host.head()
     


# In[17]:


df_host.dtypes


# In[18]:


address = []
for i in col.find( {}, {'_id':1, 'address':1}):
    address.append(i)

df_address = pd.DataFrame(address)
address_keys = list(df_address.iloc[0,1].keys())

for i in address_keys:
    if i == 'location':
        df_address['location_type'] = df_address['address'].apply(lambda x: x['location']['type'])
        df_address['longitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][0])
        df_address['latitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][1])
        df_address['is_location_exact'] = df_address['address'].apply(lambda x: x['location']['is_location_exact'])
    else:
        df_address[i] = df_address['address'].apply(lambda x: x[i] if x[i]!='' else 'Not Specified')

df_address.drop(columns=['address'], inplace=True)
df_address.head()
     


# In[19]:


df_address['is_location_exact'] = df_address['is_location_exact'].map({False:'No',True:'Yes'})
df_address.head()
     


# In[20]:


df_address.isnull().sum()


# In[21]:


df_address.dtypes


# In[22]:


availability = []
for i in col.find( {}, {'_id':1, 'availability':1}):
    availability.append(i)

df_availability = pd.DataFrame(availability)
availability_keys = list(df_availability.iloc[0,1].keys())

for i in availability_keys:
    df_availability['availability_30'] = df_availability['availability'].apply(lambda x: x['availability_30'])
    df_availability['availability_60'] = df_availability['availability'].apply(lambda x: x['availability_60'])
    df_availability['availability_90'] = df_availability['availability'].apply(lambda x: x['availability_90'])
    df_availability['availability_365'] = df_availability['availability'].apply(lambda x: x['availability_365'])

df_availability.drop(columns=['availability'], inplace=True)
df_availability.head()
     


# In[23]:


df_availability.isnull().sum()


# In[24]:


df_availability.dtypes


# In[25]:


def amenities_sort(x):
    a = x
    a.sort(reverse=False)
    return a

amenities = []
for i in col.find( {}, {'_id':1, 'amenities':1}):
    amenities.append(i)

df_amenities = pd.DataFrame(amenities)
df_amenities['amenities'] = df_amenities['amenities'].apply(lambda x: amenities_sort(x))
df_amenities.head()


# In[26]:


df_amenities.isnull().sum()


# In[27]:


df_amenities.dtypes


# In[28]:


df = pd.merge(df_1, df_host, on='_id')
df = pd.merge(df, df_address, on='_id')
df = pd.merge(df, df_availability, on='_id')
df = pd.merge(df, df_amenities, on='_id')
df.head(3)


# In[29]:


df.dtypes


# In[30]:


# download as csv
df.to_csv('airbnb.csv', index=False)







