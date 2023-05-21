import datetime as dt
import pytz

one_day = 1000 * 60 * 60 * 24

def get_bsas_time():
    return dt.datetime.now(
        tz=pytz.timezone("America/Argentina/Buenos_Aires")
    )


class ExpirationOpened:
    def __init__(self, open_time, close_time):
        self.open_time = open_time
        self.close_time = close_time

    def get_expiration(self, now, min_expiration):
        #now = get_buenos_aires_time()
        closed = None
        # monday to friday
        if 0 <= now.weekday() < 5:
            # pre
            if now.hour < self.open_time:
                closed = now.replace(minute=0, second=0, microsecond=0)
                closed -= dt.timedelta(day=3 if now.weekday() == 0 else 1)
            # market
            elif now.hour <= close_time:
                pass
            # post
            else:
                closed = now.replace(hour=18, minute=0, second=0, microsecond=0)
        else:
            closed = now.replace(hour=18, minute=0, second=0, microsecond=0)
            closed -= dt.timedelta(days=now.weekday() - 4)

        return max(
            (now - closed) / dt.timedelta(milliseconds=1),min_expiration
        )

