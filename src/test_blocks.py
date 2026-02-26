import unittest

from markdown_blocks import BlockType, block_to_block_type


class TestBlocks(unittest.TestCase):
    def test_blocks(self):
        blocks = [
            "### heading",
            "```\n this is some code \n```",
            "> first line \n>second line",
            "- first line \n- second line",
            "1. first item \n2. second item",
            "normal paragraph",
        ]
        block_types = list(map(block_to_block_type, blocks))
        result = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.ULIST,
            BlockType.OLIST,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(block_types, result)


if __name__ == "__main__":
    unittest.main()
