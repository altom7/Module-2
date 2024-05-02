import tweepy
import networkx as nx
import matplotlib.pyplot as plt

# Twitter API credentials
consumer_key = 'my_consumer_key'
consumer_secret = 'my_consumer_secret'
access_token = 'my_access_token'
access_token_secret = 'my_access_token_secret'

# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Function to collect followers of a user
def get_followers(user_id):
    followers = []
    for page in tweepy.Cursor(api.followers_ids, user_id=user_id).pages():
        followers.extend(page)
    return followers

# Function to construct a social network graph
def construct_social_network(users):
    G = nx.DiGraph()
    for user in users:
        followers = get_followers(user.id)
        for follower_id in followers:
            if follower_id in users:
                G.add_edge(follower_id, user.id)
    return G

# Function to identify influential users based on centrality metrics
def identify_influential_users(G):
    # Degree centrality
    degree_centrality = nx.degree_centrality(G)
    top_degree_users = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:5]

    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G)
    top_betweenness_users = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:5]

    # Eigenvector centrality
    eigenvector_centrality = nx.eigenvector_centrality(G)
    top_eigenvector_users = sorted(eigenvector_centrality, key=eigenvector_centrality.get, reverse=True)[:5]

    return top_degree_users, top_betweenness_users, top_eigenvector_users

# Main function
def main():
    # Seed user
    seed_user = api.get_user(screen_name='seed_user')

    # Collect followers of the seed user
    followers = get_followers(seed_user.id)

    # Construct social network graph
    G = construct_social_network(followers)

    # Identify influential users
    top_degree_users, top_betweenness_users, top_eigenvector_users = identify_influential_users(G)

    # Print results
    print("Top 5 users based on Degree Centrality:")
    print(top_degree_users)
    print("Top 5 users based on Betweenness Centrality:")
    print(top_betweenness_users)
    print("Top 5 users based on Eigenvector Centrality:")
    print(top_eigenvector_users)

    # Visualize the network graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, with_labels=True, node_size=200, font_size=8, font_color='black')
    plt.title('Social Network Graph')
    plt.show()

if __name__ == "__main__":
    main()

