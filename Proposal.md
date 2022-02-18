### Project Proposal: 
### Group 13: Jasmine Ortega, Mahsa Sarafrazi, Sufang Tan

#### Motivation and purpose

Our role: Data science consultancy firm 
Target audience: Film Studio Executives

Filming movies is an expensive and time-consuming process, so it's important that studios create movies that will appeal to large segments of the population. Netflix, one of the most popular streaming services available, is an ideal candidate for film studios to gather insights about global movie trends. We propose building a dashboard that visualizes the breadth of films that Netflix has released from 2009 to 2019. Our app will allow users to explore the trends of film genres on Netflix, film length, film-ratings (PG-13, etc), as well as filming location by country. Studio executives can use this dashboard to make decisions about which types of films will most likely appeal to streaming platforms and their audiences.


#### Description of the data


The dataset for this dashboard contains 3939 movies released on the Netflix platform from Jan 1, 2008 to Nov 30, 2019. Each movie has 12 associated variables which can be grouped into two categories: production details and Netflix details. The production variables include details about the movie itself, such as film name (`title`), director, cast, country filmed in (`country`), release year, duration, rating (ie. PG-13, R) and movie description. The Netflix variables relate to how the film is categorized and presented on the Netflix website, such as genres (`listed_in`), date added to Netflix, type ("Movie" vs Tv show) and show_id. 

Of these 12 columns, only `show_id`, `director`, `cast`, and `description` will be dropped. Time-permitting, there is room to engineer some new features from the dropped columns. For example, `cast` is not a useful feature on it's own, but could be wrangled into a `cast_count` column that counts the number of cast members in each movie.


#### Research questions you are exploring

User story:
Betty is an executive for Film In The Blank Studios. As the popularity of streaming has increased, Betty wants to understand movie streaming trends so she knows what types of movies tend to be picked up by companies like Netflix. She wants to be able to explore a dataset that compares the different genres, lengths, filming locations, and ratings of movies in order to know what kind of films Film In The Blank Studios should produce if they want to be picked up a streaming platform. 

When Betty logs onto "Netflix Movie Trends" app, she will see an overview of Netflix movies. She will be able to visualize the trends of movie ratings (ie. PG-13 or R rated film) over the span of 2008 to 2019. In comparing PG-13 and R rated movies, she will see that Netflix has released more PG-13 films than R-rated films over time. Betty also sees that two of the most popular genres on the platform are Comedy and Adventure, so she hypothesizes that Netflix prioritizes family-friendly films, such as comedic or adventure PG-13 rated films, over other categories of films. Using this information, Betty decides she will conduct a follow-up study of streaming trends on Hulu and Disney+, so she can see if the same trend is applicable across streaming platforms, or if it's just the case with Netflix. 