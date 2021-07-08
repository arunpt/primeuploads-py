import os
import shlex
import json
import asyncio
from aiohttp import ClientSession


SESSION_PATH = "primesession.json"


class PrimeException(Exception):
    pass


class PrimeUploads:
    """
    Base class which includes all the API methods
    """
    def __init__(self) -> None:
        self.api_path = "https://primeuploads.com/api/v2/"
        self.access_token = None
        self.account_id = None

    async def authorize(self, key1, key2):
        """
        Provides an access_token and account_id to make further requests into the API.

        Parameters:
            key1: The API key 1. Expected 64 characters in length.
            key2: The API key 2. Expected 64 characters in length.
        """
        data = (await self.send_data("authorize", {
            "key1": key1,
            "key2": key2
        }, True)).get("data")
        self.write_session(data)  # caching this session for future usage
        return data

    async def disable_access_token(self):
        """
        Disables an active access_token.
        """
        return await self.send_data("disable_access_token")

    async def account_info(self):
        """
        Provides details of an account based on the account_id.
        """
        return await self.send_data("account/info")

    async def account_package(self):
        """
        Provides the account restrictions inherited from the package associated to the account.
        """
        return await self.send_data("account/package")

    async def upload(self, file_path, folder_id=None):
        """
        Provides an interface to upload files. Note: There is currently no support for chunked uploads, this will be added at a later stage.

        Parameters:
            upload_file: The uploaded file.
            folder_id: A folder id within the users account. If left blank the file will be added to the root folder.
        """
        cmd = shlex.split(f"curl -X POST 'https://primeuploads.com/api/v2/file/upload' -H 'Accept: application/json' -F 'access_token={self.access_token}' -F 'account_id={self.account_id}' -F 'upload_file=@{os.path.join(file_path)}'")
        if folder_id:
            cmd.extend(["-F", f"'folder_id={folder_id}'"])
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return json.loads(stdout)

    async def download(self, file_id):
        """
        Generates a unique download url for a file.

        Parameters:
            file_id: The file id to generate the download url for.
        """
        return await self.send_data("file/download", {"file_id": file_id})

    async def file_info(self, file_id):
        """
        Provides meta data and urls of a file within a users account.

        Parameters:
            file_id: The file id to get information on.
        """
        return await self.send_data("file/info", {"file_id": file_id})

    async def edit_file(self, file_id, filename=None, file_type=None, folder_id=None):
        """
        Provides meta data and urls of a file within a users account.

        Parameters:
            file_id: The file id to update.
            filename: The new filename. Leave blank to keep existing.
            fileType: The new file type/mime type. Example: application/octet-stream. Leave blank to keep existing.
            folder_id: The new folder id in the users account. Leave blank to keep existing.
        """
        return await self.send_data("file/edit", {
            "file_id": file_id,
            "filename": filename,
            "fileType": file_type,
            "folder_id": filename
        })

    async def delete_file(self, file_id):
        """
        Delete an active file.

        Parameters:
            file_id: The file id to delete.
        """
        return await self.send_data("file/delete", {"file_id": file_id})

    async def move(self, file_id, new_parent_folder_id):
        """
        Move an active file to another folder.

        Parameters:
            file_id: The file id to move.
            new_parent_folder_id: The folder id to move the file into.
        """
        return await self.send_data("file/move", {
            "file_id": file_id,
            "new_parent_folder_id": new_parent_folder_id
        })

    async def copy(self, file_id, copy_to_folder_id):
        """
        Copy an active file to another folder.

        Parameters:
            file_id: The file id to move.
            copy_to_folder_id: The folder id to move the file into.
        """
        return await self.send_data("file/copy", {
            "file_id": file_id,
            "copy_to_folder_id": copy_to_folder_id
        })

    async def create_folder(self, folder_name, parent_id=None, is_public=0, access_password=None):
        """
        Create a new folder.

        Parameters:
            folder_name: The new folder name.
            parent_id: The folder parent id. Optional.
            is_public: Whether a folder is available publicly or private only. 0 = Private, 1 = Unlisted, 2 = Public in site search. Default Private.
            access_password: An MD5 hash of an access password. Expects 32 characters in length. Optional.
        """
        return await self.send_data("folder/create", {
            "folder_name": folder_name,
            "parent_id": parent_id,
            "is_public": is_public,
            "access_password": access_password
        })

    async def list_folders(self, parent_folder_id):
        """
        Returns a list of folders and files within the passed parent_folder_id. If this value is blank the root folder/file listing is returned.

        Parameters:
            parent_folder_id: The folder parent id. Optional.
        """
        return await self.send_data("folder/listing", {"parent_folder_id": parent_folder_id})

    async def folder_info(self, parent_folder_id):
        """
        Provides information for a specific folder id.

        Parameters:
            parent_folder_id: The folder parent id. Optional.
        """
        return await self.send_data("folder/info", {
            "parent_folder_id": parent_folder_id
        })

    async def edit_folder(self, folder_id, folder_name=None, parent_id=None, is_public=0, access_password=None):
        """
        Provides an interface to edit a folder.

        Parameters:
            folder_id: The folder id to update.
            folder_name: The new folder name. Optional.
            parent_id: The new parent id to move the folder. Optional.
            is_public: Whether a folder is available publicly or private only. 0 = Private, 1 = Unlisted, 2 = Public in site search. Optional.
            access_password: An MD5 hash of an access password. Expects 32 characters in length. Optional.
        """
        return await self.send_data("folder/edit", {
            "folder_id": folder_id,
            "folder_name": folder_name,
            "parent_id": parent_id,
            "is_public": is_public,
            "access_password": access_password
        })

    async def delete_folder(self, folder_id):
        """
        Provides an interface to delete a folder.

        Parameters:
            folder_id: The folder id to update.
        """
        return await self.send_data("folder/delete", {"folder_id": folder_id})

    async def move_folder(self, folder_id, new_parent_folder_id):
        """
        Provides an interface to move a folder.

        Parameters:
            folder_id: The folder id to update.
            new_parent_folder_id: The folder id to move the folder into.
        """
        return await self.send_data("folder/move", {
            "folder_id": folder_id,
            "new_parent_folder_id": new_parent_folder_id
        })

    async def send_data(self, endpoint, params={}, auth=False):
        api_uri = self.api_path + endpoint
        if not auth:
            params.update(access_token=self.access_token, account_id=self.account_id)  # default args
        async with ClientSession() as session:
            async with session.post(api_uri, data=params) as response:
                resp = await response.json()

        if resp.get("_status") == "success":
            return resp
        else:
            raise PrimeException(resp["response"])

    def read_session(self):
        if os.path.isfile(SESSION_PATH):
            with open(SESSION_PATH, "r") as f:
                data = json.loads(f.read())
                self.account_id = data["account_id"]
                self.access_token = data["access_token"]
            return data

    def write_session(self, data):
        self.account_id = data["account_id"]
        self.access_token = data["access_token"]
        with open(SESSION_PATH, "w") as f:
            f.write(json.dumps(data))

    async def login(self, key1, key2):
        if cached := self.read_session():
            try:
                await self.account_info()  # used to validate the saved session
                return cached
            except PrimeException:
                pass
        return await self.authorize(key1, key2)

    @property
    def creds(self):
        return dict(
            account_id=self.account_id,
            access_token=self.access_token
        )
