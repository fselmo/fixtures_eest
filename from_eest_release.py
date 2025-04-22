import tarfile
import os
import urllib.request
import argparse

cwd = os.getcwd()

parser = argparse.ArgumentParser(description="Extract EEST tests from release tarball")
parser.add_argument(
    "--version",
    type=str,
    dest="eest_version",
    default=None,
    help="Extract tests from a specific EEST release version tarball.",
)
parser.add_argument(
    "--stable",
    type=bool,
    dest="stable",
    default=False,
    help=(
        "Extract stable test fixtures. Defaults to False, extracting develop fixtures."
    ),
)

# clean existing fixtures directories
os.system("rm -rf blockchain_tests")
os.system("rm -rf blockchain_tests_engine")
os.system("rm -rf state_tests")
os.system("rm -rf transaction_tests")
os.system("rm -rf .meta")

args = parser.parse_args()
eest_version = args.eest_version.replace("v", "")
fixtures_type = "stable" if args.stable else "develop"

tarball_url = f"https://github.com/ethereum/execution-spec-tests/releases/download/v{eest_version}/fixtures_{fixtures_type}.tar.gz"  # noqa: E501
tar_path, _ = urllib.request.urlretrieve(tarball_url)

with tarfile.open(tar_path, "r:*") as tar:
    for member in tar.getmembers():
        # we only care about directories inside the ``fixtures/`` parent directory
        if member.name.startswith("fixtures/"):
            # remove the 'fixtures/' part from the path
            stripped_path = member.name[len("fixtures/") :]

            if not stripped_path:
                continue

            member.name = stripped_path
            tar.extract(member, path=cwd)
