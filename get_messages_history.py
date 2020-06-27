import vk_api
import argparse

try:
    with open("token.txt", "r") as f:
        token = f.readline().strip()
except:
    print("Error while loading configuration file, check it again!")
    exit(1)


def download_message_history(uid, filename="messages.csv", logging=True):
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    count = vk.messages.getHistory(user_id=uid)["count"]
    if logging:
        print(f"Starting to download messages from your dialog with user {uid} from Vkontakte")
    with open(filename, "w") as f:
        f.write("id\ttimestamp\ttext\thas_fwd\thas_attachments\tis_out\n")
        for offset in range(0, count, 200):
            result = vk.messages.getHistory(user_id=uid, offset=offset, count=200)
            messages = result["items"]
            if logging:
                print(f"\rProgress: {round(offset / count * 100, 2)}%               ", end="")
            for message in messages:
                if not message["text"]:
                    continue
                mid = message["id"]
                timestamp = message["date"]
                text = message["text"].replace("\n", " ")
                has_fwd = int(message["fwd_messages"] != [])
                has_attachments = int(message["attachments"] != [])
                is_out = int(message["out"])
                f.write(f"{mid}\t{timestamp}\t{text}\t{has_fwd}\t{has_attachments}\t{is_out}\n")
    if logging:
        print("\rCompleted!                ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download dialog history with user in Vkontakte")
    parser.add_argument("--uid", "-u", type=int, help="Vk user id (i.e., 154941750)")
    parser.add_argument("--filename", "-f", type=str, help="File destination (i.e., messages.csv)",
                        default="messages.csv")
    parser.add_argument("--quiet", "-q", help="Quiet mode with no logging", action="store_const",
                        const=True, default=False)

    args = parser.parse_args()
    if args.uid is None:
        args.uid = input("Input uid in vk: ")

    download_message_history(uid=args.uid, filename=args.filename, logging=(not args.quiet))
