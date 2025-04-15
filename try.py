from mcp.server.fastmcp import FastMCP;
import logging;
logging.basicConfig(level=logging.DEBUG);
FastMCP('test', log_level='DEBUG').run(transport='stdio')