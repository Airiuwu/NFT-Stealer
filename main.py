from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
import requests, os, time, asyncio, math

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()
headers = {'User-Agent': user_agent, "Accept": "application/json"}
ipfs_gateways = [
  'cf-ipfs.com', 'gateway.ipfs.io',
  'cloudflare-ipfs.com', '10.via0.com',
  'gateway.pinata.cloud', 'ipfs.cf-ipfs.com',
  'ipfs.io', 'ipfs.sloppyta.co',
  'ipfs.best-practice.se', 'snap1.d.tube',
  'ipfs.greyh.at', 'ipfs.drink.cafe',
  'ipfs.2read.net', 'robotizing.net',
  'dweb.link', 'ninetailed.ninja'
]

async def load():
    for dot in ('.', '..', '...'):
        os.system('cls')
        print(f'Hacking into the NFT database{dot}')
        time.sleep(0.3)

async def preformStartup(collection):
    os.system('cls')
    print('███    ██ ███████ ████████     ███████ ████████ ███████  █████  ██      ███████ ██████')
    print('████   ██ ██         ██        ██         ██    ██      ██   ██ ██      ██      ██   ██')
    print('██ ██  ██ █████      ██        ███████    ██    █████   ███████ ██      █████   ██████')
    print('██  ██ ██ ██         ██             ██    ██    ██      ██   ██ ██      ██      ██   ██')
    print('██   ████ ██         ██        ███████    ██    ███████ ██   ██ ███████ ███████ ██   ██')
    time.sleep(3)
    os.system('cls')
    for directory in ('./NFTs', f'./NFTs/{collection}'):
        if not os.path.exists(directory):
            os.mkdir(directory)
    for i in range(2):
        await load()

async def resolve_ipfs(image_url):
  cid = image_url.removeprefix("ipfs://")
  for gateway in ipfs_gateways:
    request = requests.get(f"https://{gateway}/ipfs/{cid}")
    if request.status_code == 200:
      break
  return request

async def main():
    os.system('cls')
    print('Please input which OpenSea Collection you would like to steal.')
    collection_name = input()
    await preformStartup(collection=collection_name)
    collection = requests.get(f"http://api.opensea.io/api/v1/collection/{collection_name}?format=json")
    collection_data = collection.json()
    if collection.status_code == 404:
        print(f'The collection {collection_name} was not found!')
        exit()

    amount = 0
    for i in range(math.ceil(collection_data['collection']['stats']['count'] / 50)):
        count = i * 50
        NFT_data = requests.get(f'https://api.opensea.io/api/v1/assets?order_direction=asc&offset={count}&limit=50&collection={collection_name}&format=json', headers=headers).json()
        for token in NFT_data['assets']:
            number_formatted = f'{int(token["token_id"])}'
            if os.path.exists(f'./NFTs/{collection_name}/{number_formatted}.png'):
                print('Keep your head in the game. We already stole this NFT.')
            else:
                image_url = token['image_url']
                if image_url.startswith('ipfs://'):
                    image_url = await resolve_ipfs(image_url).url
                image = requests.get(image_url)
                if image.status_code == 200:
                    with open(f'./NFTs/{collection_name}/{number_formatted}.png', 'wb') as file:
                        file.write(image.content)
                        file.close()
                        print(f'Good work, you\'ve stole NFT number {number_formatted}.')
                        amount += 1
                else:
                    print(f'Dang it, we lost that one. => {number_formatted}')
                    continue
    print(f'Good work soldier, you\'ve managed to get {count} NFTs.\nYou can view your newly acquired NFTs in ./NFTs/{collection_name}')

asyncio.run(main())
