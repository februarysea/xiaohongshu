# Clean data and enerate .csv data
import csv
import json



def generate_data():
    # Return a dict list
    error_lines = []
    error_details = []
    notes = []
    users = []
    data = []
    count = 1

    with open('notes.txt', 'r') as f:
        for line in f.readlines():
            notes.append(line)
    with open('noteUsers.txt', 'r') as f:
        for line in f.readlines():
            users.append(line)
    for note, user in zip(notes, users):
        try:
            note = note.replace("\'", "\"")
            note = note.replace("\\n", "")
            user = user.replace("\'", "\"")
            note = json.loads(note)
            user = json.loads(user)
            note.update(user)
        except Exception as e:
            error_lines.append(count)
            error_details.append(e)
        else:
            data.append(note)
        finally:
            count = count + 1

    # Get data error line and details
    #print(error_lines)
    #print(error_details)
    return data

def data_to_csv(data):
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["author_collect_nr","author_fans_nr","author_name","author_note_nr","comment_nr","content","datePublished","images","like_nr","star_nr","title","url","user_url"])
        for item in data:
            writer.writerow([item["author_collect_nr"], item["author_fans_nr"], item["author_name"], item["author_note_nr"], item["comment_nr"], item["content"], item["datePublished"], item["images"], item["like_nr"], item["star_nr"], item["title"], item["url"], item["user_url"]])

if __name__ == '__main__':
    data = generate_data()
    data_to_csv(data)