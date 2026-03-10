from jinja2 import Environment, DictLoader, select_autoescape

templates = {
    "trade_alert": """
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2e6c80;">Trade Alert</h2>
        <p>A trade has been executed.</p>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr>
                <th>Action</th>
                <td>{{ trade.action }}</td>
            </tr>
            <tr>
                <th>Symbol</th>
                <td>{{ trade.symbol }}</td>
            </tr>
            <tr>
                <th>Quantity</th>
                <td>{{ trade.quantity }}</td>
            </tr>
            <tr>
                <th>Price</th>
                <td>{{ trade.price }}</td>
            </tr>
            <tr>
                <th>Strategy</th>
                <td>{{ trade.strategy }}</td>
            </tr>
            <tr>
                <th>Time</th>
                <td>{{ trade.time }}</td>
            </tr>
        </table>
      </body>
    </html>
    """,
    "error_alert": """
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #c92a2a;">Bot Error Alert</h2>
        <p>The bot encountered an error:</p>
        <div style="background-color: #f8d7da; padding: 10px; border-left: 5px solid #c92a2a;">
            <strong>Error Details:</strong>
            <p>{{ error_msg }}</p>
        </div>
      </body>
    </html>
    """,
    "bot_start": """
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2b8a3e;">Bot Started Successfully</h2>
        <p>The trading bot has started and is now monitoring the markets.</p>
        <p><strong>Time:</strong> {{ time }}</p>
      </body>
    </html>
    """
}

env = Environment(
    loader=DictLoader(templates),
    autoescape=select_autoescape(['html', 'xml'])
)

def get_template(name: str):
    return env.get_template(name)
