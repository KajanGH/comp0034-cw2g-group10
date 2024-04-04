import csv
import jwt
import sys
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from flask import make_response, current_app as app, request, session, render_template
from functools import wraps

USERS_FILE = 'dataset\\users.csv'

def encode_auth_token(id):
    """Generates the Auth Token."""
    try:
        token = jwt.encode(
        payload={
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "iat": datetime.now(timezone.utc),
            "sub": id,
        },
        key=app.secret_key,
        algorithm='HS256',
    )
        return token
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """Decodes the auth token."""
    try:
        payload = jwt.decode(auth_token, app.secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return make_response({'message': "Token expired. Please log in again."}, 401)
    except jwt.InvalidTokenError:
        return make_response({'message': "Invalid token. Please log in again."}, 401)


def get_user(id,users):
    """Get user details from CSV."""
    df = pd.read_csv(users)
    if id in df['id'].values:
        return df[df['id'] == id].to_dict('records')[0]
    return None


def token_required(f):
    """Require valid jwt for a route."""
    @wraps(f)
    def decorator(*args, **kwargs):
        if "token" in session.keys(): token = session['token']
        else: token = None
        if not token: return render_template('log-in-page.html',error="Authentication Token missing, please log in")
        token_payload = decode_auth_token(token)
        try: id = token_payload["sub"]
        except TypeError: return render_template('log-in-page.html', error = "Authentication Token expired, please log in again")
        user = get_user(id,USERS_FILE)
        if not user: return render_template('log-in-page.html',error="Invalid or missing user id, please log in again")

        return f(*args, **kwargs)
    return decorator

def trends_box(sexChoice, formatted_date, selected_layer):
    formatted_date = int(formatted_date.split('-')[0])
    comparison_date = formatted_date - 1

    if selected_layer == 'rgn':
        geocolumn = "Region"
        data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_Region_sex_age_group.csv')
    elif selected_layer == 'lad':
        geocolumn = "LAD"
        data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_LAD_sex_age_group.csv')
    elif selected_layer == 'itl':
        geocolumn = "ITL"
        data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_ITL_sex_age_group.csv')

    # First year:
    fdata = data[data['sex'] == sexChoice]
    fdata = fdata[fdata['extract_date'].str.contains(str(formatted_date))]
    if (selected_layer == 'lad' or selected_layer == 'itl') and filter == 1:
        fdata = fdata[fdata['Region'] == 'London']
        if selected_layer == 'lad':
            fdata = fdata[fdata['ITL'] == fdata['ITL']]

    # Group by 'Region' and sum the age columns
    fdata = fdata.groupby(geocolumn).sum()

    # Reset the index to make 'Region' a column again
    fdata.reset_index(inplace=True)
    age_columns = [col for col in fdata.columns if col.startswith('age_')]
    fdata[f'{formatted_date}total_age'] = fdata[age_columns].sum(axis=1).astype(float)

    # Reference year:
    cdata = data[data['sex'] == sexChoice]
    cdata = cdata[cdata['extract_date'].str.contains(str(comparison_date))]
    if (selected_layer == 'lad' or selected_layer == 'itl') and filter == 1:
        cdata = cdata[cdata['Region'] == 'London']
        if selected_layer == 'lad':
            cdata = cdata[cdata['ITL'] == cdata['ITL']]

    # Group by 'Region' and sum the age columns
    cdata = cdata.groupby(geocolumn).sum()

    # Reset the index to make 'Region' a column again
    cdata.reset_index(inplace=True)
    age_columns = [col for col in cdata.columns if col.startswith('age_')]
    cdata[f'{comparison_date}total_age'] = cdata[age_columns].sum(axis=1).astype(float)

    # Merge the two dataframes on 'Region'
    fdata = fdata.merge(cdata, on=geocolumn, how='left')

    # Calculate the percentage change and add it as a new column
    fdata['change'] = ((fdata[f'{formatted_date}total_age'] - fdata[f'{comparison_date}total_age']) / fdata[f'{comparison_date}total_age']) * 100

    # Round the 'change' values to 2 significant figures
    fdata['change'] = fdata['change'].round(2)

    # Sort by 'change' column in descending order
    fdata.sort_values('change', ascending=False, inplace=True)

    # Convert to nested list
    fdata = fdata.head(8)[[geocolumn, 'change']].values.tolist()

    return fdata
