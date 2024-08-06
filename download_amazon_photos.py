"""
Download photos from Amazon Photos via API
"""
import logging
import socket
from amazon_photos import AmazonPhotos

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def resolve_hostname(hostname):
    """
    Resolves the host name
    """
    try:
        ip_address = socket.gethostbyname(hostname)
        logger.info("Resolved {} to {}".format(hostname, ip_address))
        return ip_address
    except socket.gaierror as e:
        logger.error("Failed to resolve hostname {}: {}".format(hostname, e))
        return None

def create_amazon_photos_instance():
    """
    Creates an Amazon Photos instance
    """
    try:
        # Verify that the hostnames can be resolved
        if not resolve_hostname('amazon.com'):
            raise Exception("Failed to resolve amazon.com")
        if not resolve_hostname('drive.amazonaws.com'):
            raise Exception("Failed to resolve drive.amazonaws.com")

        # TODO The error is occuring inside this class - need to get visibility of what's happening
        ap = AmazonPhotos(
            cookies={
                'ubid-acbuk' : "261-8674950-0497261",
                'at-acbuk' : "Atza|IwEBIBPwkXydmZKksJXvoprkkw8PHmY0fpdvhW7arxZhNdsNhrx0ytJOmFvD108c8clCrllm04-N78QNjMmADyAA0PaZcGVlcvGBoNIL8Yy4XufhD2ZHx9MtgVFq7nEQbUw38Kw_kKcapey98Ofx1yqWKD1tCpX3n8TVc6X2eaTyc7pDqj_GPfaGGGIaHab7RvemLrNio_-csGeo4Ui7Nm8lCoWodnKIstjDymm6Jl3FTx4RSZ3bDz259tG31lBmx4YOutY",
                'session-id' : "259-0361404-2778530",
            },
        )
        return ap
    except Exception as e:
        logger.error("Failed to create AmazonPhotos instance: {}".format(e), exc_info=True)
        return None

def main():
    """
    Main method
    """
    ap = create_amazon_photos_instance()
    if ap is None:
        logger.error("AmazonPhotos instance creation failed")
        return

    try:
        # get current usage stats
        ap.usage()

        # get entire Amazon Photos library
        print("get entire Amazon library")

        nodes = ap.query("type:(PHOTOS OR VIDEOS)")

        num_nodes = len(nodes)
        print("{:0d} nodes".format(num_nodes))

        # sample first 10 nodes
        node_ids = nodes.id[:10]
        print(node_ids)

        # Example function to get folder structure (you need to replace this with actual function calls)
        folder_structure = ap.get_folder_structure()
        logger.info("Folder structure: %s", folder_structure)
    except AttributeError as e:
        logger.error("AttributeError: %s", e)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()

