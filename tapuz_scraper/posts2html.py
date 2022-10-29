import json
import datetime
import argparse

TEMPLATE = """
<!doctype html>
<html lang="he" dir="rtl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        <title>הודעות</title>

        <style>
        .post {{
            border: 2px solid gray;
            margin: 45px;
            padding: 5px;
        }}

        h1 {{
            text-align: center;
        }}

        h3 {{
            text-align: center;
            font-size: 1em;
        }}
        </style>
    </head>
    <body>
        <h1>הודעות</h1>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

        <h2>אינדקס</h2>
        <ul>
            {index}
        </ul>

        <h2>תוכן</h2>
        <div class="container">
        {messages}
        </div>
    </body>
</html>

"""

def main(input_file, output_file) -> None:
    data = json.load(input_file)
    
    output = ""
    counter = 0
    titles = []

    for post in data:
        counter += 1

        titles.append(f"            <li><a href='#post_{counter}'>{post['title']}</a></li>")

        output += f"            <div class='post' id='post_{counter}'>\n"
        output += f"                <h3><a href='https://www.tapuz.co.il/threads/{post['id']}' target='_BLANK'>{post['title']}</a></h3>"
        for message in post["messages"]:
            content = message["content"].replace('\n', '<br/>')
            output += f"""
                <div class="row">
                    <div class="col-md-12">
                        <div class="card mb-4">
                            <div class="card-header">
                                <div class="media flex-wrap w-100 align-items-center">
                                    <div class="media-body ml-3">
                                        {message["author"]}
                                    </div>
                                    <div class="text-muted small ml-3">
                                        {datetime.datetime.fromtimestamp(int(message["date"]))}
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                {content}
                            </div>
                        </div>
                    </div>
                </div>
            """
        output += "            </div>\n"



    output_file.write(TEMPLATE.format(messages = output, index = "\n".join(titles)))
    print(f"Processed {counter} post(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A basic formatter for the Tapuz Forum Scraper. '
                                                 'This script formats the output of the scraper as basic HTML.')
    parser.add_argument('-i', '--infile', type=argparse.FileType('r', encoding='UTF-8'), required=True, 
                        help="Path to input file.\nThis file should contains all the posts in JSON format.")
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w', encoding='UTF-8'), required=True,
                        help="Path to output file.\nThis file will contain a basic HTML representation of the given posts.")
    args = parser.parse_args()
    main(args.infile, args.outfile)