import statistics
import plotly.graph_objects as go
import unicodedata
import plotly.io as pio


def normalize_persian_text(text):
    return unicodedata.normalize("NFKC", text)


def validate_title_by_keywords(title, keyword_groups):
    # Normalize the title
    normalized_title = normalize_persian_text(title)

    # Check each group of keywords
    for group in keyword_groups:

        if not any(
            normalize_persian_text(keyword) in normalized_title for keyword in group
        ):
            return False
    return True


def create_html_plot(posts, keyword_groups, show=False):

    # Filter posts based on the keyword groups in the title
    posts = [
        post
        for post in posts
        if validate_title_by_keywords(post["title"], keyword_groups)
    ]

    # compute stats
    worked = [post["worked"] for post in posts]
    price = [post["price"] for post in posts]
    mean_worked = statistics.mean(worked)
    median_price = statistics.median(price)

    # Prepare data for plotting (using all posts, no filtering)
    x_values = [post["worked"] for post in posts]  # worked values (x-axis)
    y_values = [post["price"] for post in posts]  # price values (y-axis)

    # color as the year of build
    colors = [post["year"] for post in posts]

    # link to each post
    urls = [post["url"] for post in posts]

    # Hover text with relevant info
    texts = [
        f"Title: {post['title']}<br>Worked: {post['worked']}<br>Price: {post['price']} تومان<br>Year: {post['year']}<br><a href='{post['url']}' target='_blank'>Click to View</a>"
        for post in posts
    ]

    # Create scatter plot
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="markers",
            marker=dict(
                size=15,  # Size of points based on year
                color=colors,  # Color of the points
                opacity=0.7,  # Marker opacity
                showscale=True,  # Display color scale
            ),
            text=texts,  # Hover text
            hoverinfo="text",  # Show only hover text
            customdata=urls,
        )
    )

    # Set axes limits based on 2 standard deviations from the mean
    fig.update_layout(
        title="Car Listings: Worked vs Price",
        xaxis_title="Worked (km)",
        yaxis_title="Price (Toman)",
        showlegend=False,
        template="plotly_white",  # Optional, change for a darker theme
        xaxis=dict(
            range=[
                0,
                3 * mean_worked,
            ],  # Set x-axis to ± 2 std from mean
        ),
        yaxis=dict(
            range=[
                median_price - 70_000_000,
                median_price + 70_000_000,
            ],  # Set y-axis to ± 2 std from mean
        ),
    )

    # JavaScript callback to open URL on click
    click_js = """
    <script>
        var plot = document.getElementsByClassName('plotly-graph-div')[0];
        plot.on('plotly_click', function(data){
            var url = data.points[0].customdata;
            window.open(url);
        });
    </script>
    """

    # create html for plotting
    html_str = pio.to_html(fig, include_plotlyjs="cdn", full_html=True)
    html_with_js = html_str.replace("</body>", f"{click_js}</body>")

    if show:
        fig.show()

    return html_with_js
