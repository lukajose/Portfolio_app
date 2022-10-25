from stake import StakeClient, SessionTokenLoginRequest, CredentialsLoginRequest
import stake
import asyncio
import os



print(os.getenv("STAKE_TOKEN"))
login_request = SessionTokenLoginRequest(token=os.getenv("STAKE_TOKEN"))

async def print_user():
    async with StakeClient(login_request) as stake_session:
        print(stake_session.user.first_name)
        print(stake_session.headers.stake_session_token)



async def show_portfolio():
    # here the client will use the STAKE_TOKEN env var for authenticating
    async with StakeClient(login_request) as stake_session:
        my_equities = await stake_session.equities.list()
        for my_equity in my_equities.equity_positions:
            print(my_equity.symbol, my_equity.yearly_return_value)
        return my_equities

asyncio.run(print_user())
asyncio.run(show_portfolio())