# Importing necessary modules
import argparse
import sys
import os

if len(sys.argv) < 1:
    print("usage: python edit_links.py <add|del> [args]")
    sys.exit(1)

# Checking if the script is being run from the correct directory (jmp or autoslug.github.io)
if os.path.basename(
    os.path.dirname(os.path.realpath(__file__))
) != "jmp" and "jmp" not in os.listdir("."):
    print(
        "Please run this script from the jmp directory or the autoslug.github.io repository root"
    )
    sys.exit(1)
elif "jmp" not in os.listdir("."):
    os.chdir("..")

if len(sys.argv) < 2:
    print("usage: python edit_links.py <action> <short> [long] [description]")
    sys.exit(1)

# use argparse to get an add/del argument, a short, long, and description argument for add, and a short argument for del
parser = argparse.ArgumentParser()
parser.add_argument("action", help="add or del")
parser.add_argument("short", help="short link to add or delete")
parser.add_argument(
    "long",
    help="full url of the link, required if adding",
    nargs="?" if sys.argv[1] == "del" else 1,
)
parser.add_argument(
    "description",
    help="description of the link, required if adding",
    nargs="?" if sys.argv[1] == "del" else 1,
)
args = parser.parse_args()

# Checking if the user wants to add a new link
if args.action == "add":
    # Checking if the user has provided all the required arguments
    # if len(sys.argv) != 5:
    #     print("usage: python edit_links.py add <short> <long> <description>")
    #     sys.exit(1)

    # Assigning the arguments to variables
    short = args.short
    long = args.long[0]
    description = args.description[0]

    # Generating the HTML code for the redirect
    html = '<meta http-equiv="Refresh" content="0; url=\'' + long + "'\" />"

    # Checking if the link already exists
    if short in os.listdir("."):
        print("Error: link '" + short + "' already exists")
        sys.exit(1)

    # Creating a new folder with the short name and adding an index.html file inside containing the HTML code
    os.mkdir(short)
    f = open(short + "/index.html", "w")
    f.write(html)
    f.close()

    # Adding the new link to the jmp/index.html table
    f = open("jmp/index.html", "r")
    lines = f.readlines()
    f.close()
    f = open("jmp/index.html", "w")
    for line in lines:
        # Checking if the line contains the end of the table
        if "</table>" in line:
            # Adding the new link to the table
            f.write(
                "        <tr>\n"
                + '            <th><a href="../'
                + short
                + '">'
                + short
                + "</a></th>\n"
                + "            <td>"
                + description
                + "</td>\n"
                + "        </tr>\n"
            )
        f.write(line)
    f.close()

# Checking if the user wants to delete a link
elif args.action == "del":
    # Checking if the user has provided all the required arguments
    # if len(sys.argv) != 3:
    #     print("usage: python edit_links.py del <short>")
    #     sys.exit(1)

    # Assigning the arguments to variables
    short = args.short

    # delete folder with [short] name if it exists
    try:
        os.remove(short + "/index.html")
        os.rmdir(short)
    except FileNotFoundError:
        print("Error: link '" + short + "' does not exist")
        sys.exit(1)

    # delete link from jmp/index.html table
    f = open("jmp/index.html", "r")
    lines = f.readlines()
    f.close()
    f = open("jmp/index.html", "w")

    # parse through lines and delete the <tr> with the link
    linenum = 0
    for i, line in enumerate(lines):
        # if currently on one of the lines of the <tr> with the link, skip it
        if linenum > 0 and linenum < 4:
            linenum += 1
        # if the next line has the link, the current line is the beginning of the relevant <tr>
        elif (
            i < len(lines) - 1
            and '<th><a href="../' + short + '">' + short + "</a></th>" in lines[i + 1]
        ):
            linenum = 1
        # if the next line does not have the link or the current line is after the last line of the <tr> to be deleted, write the current line
        else:
            linenum = 0
            f.write(line)
    f.close()
