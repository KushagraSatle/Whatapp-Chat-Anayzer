import re
import pandas as pd


def preprocess(data):

    pattern = r'\[?\s*(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}:\d{2})[\s\u202f]*(AM|PM)\]\s*'

    matches = list(re.finditer(pattern, data))

    rows = []

    for i, match in enumerate(matches):

        date = match.group(1)
        time = match.group(2)
        am_pm = match.group(3)

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(data)

        message = data[start:end].strip()

        # Remove invisible character
        message = message.replace('\u200e', '').strip()

        # Separate user and message
        if ': ' in message:
            user, msg = message.split(': ', 1)
        else:
            user = 'group_notification'
            msg = message

        rows.append({
            'date': date,
            'time': time,
            'am_pm': am_pm,       # <-- IMPORTANT
            'user': user,
            'message': msg
        })

    df = pd.DataFrame(rows)

    # Convert into datetime
    df['date'] = pd.to_datetime(
        df['date'] + ' ' +
        df['time'] + ' ' +
        df['am_pm'],
        format='%d/%m/%y %I:%M:%S %p'
    )

    # Remove unnecessary columns
    df.drop(columns=['time', 'am_pm'], inplace=True)

    return df