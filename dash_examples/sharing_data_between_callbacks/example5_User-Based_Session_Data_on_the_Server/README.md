# User-Based Session Data on the Server

The previous example4 cached computations in a way that was accessible for all users.

Sometimes you may want to keep the data isolated to user sessions: one user's derived data shouldn't update the next user's derived data. One way to do this is to save the data in a dcc.Store, as demonstrated in the first example.

Another way to do this is to save the data in a cache along with a session ID and then reference the data using that session ID. Because data is saved on the server instead of transported over the network, this method is generally faster than the dcc.Store method.

## This example

- Caches data using the flask_caching filesystem cache. You can also save to an in-memory cache or database such as Redis instead.
Serializes the data as JSON.

- If you are using Pandas, consider serializing with Apache Arrow for faster serialization or Plasma for smaller dataframe size. Community thread

- Saves session data up to the number of expected concurrent users. This prevents the cache from being overfilled with data.

- Creates unique session IDs for each session and stores it as the data of dcc.Store **on every page load**. This means that every user session has unique data in the dcc.Store on their page.

## Notes

- The timestamps of the dataframe don't update when we retrieve the data. This data is cached as part of the user's session.

- Retrieving the data initially takes three seconds but successive queries are instant, as the data has been cached.

- The second session displays different data than the first session: the data that is shared between callbacks is isolated to individual user sessions.
