
from pathlib import Path
import csv
import os

import sqlalchemy.exc as sa_exc
from top_memory import database as db


def get_lines(file, lower=True):
    try:
        with open(file, 'r', encoding='utf8') as h:
            for line in h:
                line = line.strip()
                if line:
                    if lower:
                        yield line.lower()
                    else:
                        yield line
    except FileNotFoundError:
        print(f'Warning: does not exist: {file}')
    except UnicodeDecodeError:
        print(f'Unicode error: ' + str(file))


def add_words(session, words_dir):
    """Update database of words"""
    for entry in words_dir.iterdir():
        if entry.is_dir():
            concrete_noun = set(get_lines(entry / 'concrete_noun.txt'))
            abstract_noun = set(get_lines(entry / 'abstract_noun.txt'))
            infinitive_verb = set(get_lines(entry / 'infinitive_verb.txt'))
            words = concrete_noun | abstract_noun | infinitive_verb

            language = db.Language.find_or_add(session, entry.stem)
            for word in language.words:
                # For each word in the database for this language,
                # we want to check if we need to modify or delete it.

                if word.value in words:
                    # MODIFY
                    words.remove(word.value)  # Done with this word, delete it
                    word.concrete_noun = word.value in concrete_noun
                    word.abstract_noun = word.value in abstract_noun
                    word.infinitive_verb = word.value in infinitive_verb
                    session.add(word)
                else:
                    # DELETE
                    session.delete(word)

            # The remaining words needs to be added to the database
            for word in words:
                # NEW
                language.words.append(db.Word(
                    word,
                    word in concrete_noun,
                    word in abstract_noun,
                    word in infinitive_verb
                ))


def add_stories(session, stories_dir):
    """Update database of stories"""
    for entry in stories_dir.iterdir():
        if entry.is_file():
            stories = set(get_lines(entry, lower=False))
            language = db.Language.find_or_add(session, entry.stem)
            for story in language.stories:
                if story.value in stories:
                    # Already in database, all good, discard story
                    stories.remove(story.value)
                else:
                    # Delete
                    session.delete(story)

            # The remaining stories needs to be added to the database
            for story in stories:
                if len(story.split()) > 6:
                    print(f'Too many words: {story}')
                    continue
                language.stories.append(db.Story(story))


def add_image_files(session, images_dir):
    """Update database of Face Files"""

    d = dict()
    for file in session.query(db.ImageFile).all():
        d[file.md5] = file

    extensions = ('.jpg', '.png')
    for path, dirs, files in os.walk(images_dir):
        for file in files:
            file = Path(path) / file
            if file.suffix not in extensions:
                print(f'Warning: extension wrong. file skipped: {file.name}')
                continue
            img = db.ImageFile(file)
            if img.md5 in d:
                db_img = d[img.md5]
                db_img.filename = img.filename
                session.add(db_img)
                del d[img.md5]
            else:
                session.add(img)
    for md5 in d:
        session.delete(d[md5])


def add_face_files(session, images_dir):
    """Update database of Face Files"""

    d = dict()
    for file in session.query(db.FaceFile).all():
        d[file.md5] = file

    extensions = ('.jpg', '.png')
    for path, dirs, files in os.walk(images_dir):
        for file in files:
            file = Path(path) / file
            if file.suffix not in extensions:
                print(f'Warning: extension wrong. file skipped: {file.name}')
                continue
            img = db.FaceFile(file)
            if img.md5 in d:
                db_img = d[img.md5]
                db_img.filename = img.filename
                db_img.gender = img.gender
                session.add(db_img)
                del d[img.md5]
            else:
                session.add(img)
    for md5 in d:
        session.delete(d[md5])


def add_firstnames(session, names_dir):
    """Update database of firstnames"""
    for region_type in db.RegionType:
        # Create the Region instance
        region = db.Region.find_or_add(session, region_type)

        # Get name directories
        female = names_dir / region_type.name / 'firstname_female'
        male = names_dir / region_type.name / 'firstname_male'
        unisex = names_dir / region_type.name / 'firstname_unisex'

        # Grab all names for each gender
        female_names = set()
        for file in female.glob('*.txt'):
            female_names |= set(get_lines(file, lower=False))

        male_names = set()
        for file in male.glob('*.txt'):
            male_names |= set(get_lines(file, lower=False))

        unisex_names = set()
        for file in unisex.glob('*.txt'):
            unisex_names |= set(get_lines(file, lower=False))

        names = female_names | male_names | unisex_names

        for name in region.firstnames:
            # For each word in the database for this language,
            # we want to check if we need to modify or delete it.

            if name.value in names:
                # MODIFY
                names.remove(name.value)  # Done with this name, delete it
                if (name.value in female_names and name.value in male_names) \
                        or name.value in unisex_names:
                    name.gender = db.Gender.unisex
                elif name.value in female_names:
                    name.gender = db.Gender.female
                elif name.value in male_names:
                    name.gender = db.Gender.male
                session.add(name)
            else:
                # DELETE
                session.delete(name)

        # The remaining words needs to be added to the database
        for name in names:
            # NEW
            if (name in female_names and name in male_names) \
                    or name in unisex_names:
                gender = db.Gender.unisex
            elif name in female_names:
                gender = db.Gender.female
            elif name in male_names:
                gender = db.Gender.male

            firstname = db.FirstName(name, gender)
            session.add(firstname)
            region.firstnames.append(firstname)


def add_lastnames(session, names_dir):
    """Update database of lastnames"""
    for region_type in db.RegionType:
        # Create the Region instance
        region = db.Region.find_or_add(session, region_type)
        lastname_dir = names_dir / region_type.name / 'lastname'
        lastnames = set()
        for file in lastname_dir.glob('*.txt'):
            lastnames |= set(get_lines(file, lower=False))

        for ln in region.lastnames:
            if ln.value in lastnames:
                # Already in database, all good, discard story
                lastnames.remove(ln.value)
            else:
                # Delete
                session.delete(ln)

        # The remaining lastnames needs to be added to the database
        for value in lastnames:
            lastname= db.LastName(value)
            session.add(lastname)
            region.lastnames.append(lastname)


def add_disciplines(session, csv_file):

    def float_if_not_null(x):
        if x == 0:
            return x
        return float(x) if x else None

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            q = session.query(db.Discipline)
            q = q.filter_by(discipline=row.get('discipline'))
            d = q.first()
            if d is None:
                d = db.Discipline()
                d.discipline = row.get('discipline')
            d.type_ = row.get('type')
            d.name = row.get('name')
            d.memo_time = int(row.get('memo_time'))
            d.recall_time = int(row.get('recall_time'))
            d.world = int(row.get('world'))
            d.international = int(row.get('international'))
            d.national = int(row.get('national'))
            d.standard_k0 = float_if_not_null(row.get('standard_k0'))
            d.standard_k1 = float_if_not_null(row.get('standard_k1'))
            session.add(d)


def add_test_users(session):
    for i in range(10):
        name = f'test_user_{i}'
        u = session.query(db.User).filter_by(username=name).first()
        if u is None:
            u = db.User(session,
                username=name,
                password=name,
                email=f'{name}@penlect.com',
                firstname=f'Firstname_{i}',
                lastname=f'Lastname_{i}',
                country=f'Country_{i}',
                blocked=bool(i%2)
            )
            session.add(u)
    name = 'admin'
    u = session.query(db.User).filter_by(username=name).first()
    if u is None:
        u = db.User(session,
            username=name,
            password='melodiesoflife',
            email='',
            firstname=f'Daniel',
            lastname=f'Andersson',
            country=f'Sweden',
            blocked=False
        )
        session.add(u)


def synchronize(session, root):

    add_disciplines(session, root / 'standard.csv')

    add_words(session, root / 'words')
    add_stories(session, root / 'historical')
    add_image_files(session, root / 'img' / 'random-images')
    add_face_files(session, root / 'img' / 'profile-images')
    add_firstnames(session, root  / 'names')
    add_lastnames(session, root / 'names')

    add_test_users(session)


if __name__ == '__main__':
    root = Path(__file__).parent
    engine = db.get_dummy_engine()
    session = db.get_session(engine, create_tables=True)

    synchronize(session, root)
    try:
        session.commit()
    except sa_exc.IntegrityError:
        session.rollback()
    else:
        session.close()
