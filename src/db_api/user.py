from sqlalchemy import func
from schema.users import Users

def get(session, filters):
    errors = []
    if not filters:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    try:
        user = session.query(Users).filter_by(**filters).one()
    except Exception as e:
        errors.append(e)
        user = None
    return {'errors': errors, 'result': user}

def get_all(session, offset=None, limit=None):
    errors = []
    try:
        users = session.query(Users).order_by(Users.id)
        if limit:
            users = users.limit(limit)

        if offset:
            offset -= 1
            users = users.offset(offset*limit)
    except Exception as e:
        errors.append(e)
        users = None
    return {'errors': errors, 'result': users}

def count(session):        
    return session.query(func.count(Users.id)).scalar() 

def update(session, data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    try:
        if data.get('user_id'):
            user = session.query(Users).filter(Users.user_id == data['user_id']).update(data['update'])
        elif data.get('id'):
            user = session.query(Users).filter(Users.id == data['id']).update(data['update'])
        else:
            errors.append('User not found')
            user = None
        result = 1
        session.commit()
    except Exception as e:
        errors.append(e)
        result = 0

    return {'errors': errors, 'result': result}

def create(session, data, commit=True):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    try:
        user = Users(
            user_id=data['user_id'],
            name=data['name'],
            clean_name=data['clean_name'],
            reputation=data['reputation'],
            website=data.get('website', ''),
            location=data.get('location', '')[:80],
            about_me=data.get('about_me', ''),
            views=data.get('views', 0),
            up_votes=data.get('up_votes', 0),
            account_id=data.get('account_id', 0),
            down_votes=data.get('down_votes', 0),
            last_access_time=data.get('last_access_time'),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        result = 1
        if commit:
            session.add(user)
            session.commit()
    except Exception as e:
        session.rollback()
        errors.append(e)
        result = 0
        user = None

    return {'errors': errors, 'result': result, 'user': user}