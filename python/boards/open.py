import vim
import sys
from ..common.connection import Connection
from ..common.kanbanBoard import KanbanBoard

connection = Connection.getConnectionFromVars()

# arguments expected in sys.argv
def JiraVimBoardOpen():
    boardName = str( sys.argv[0]) 
    board = connection.getBoard(boardName)
    issues = board.getIssues()

    # Buff Setup Commands
    vim.command("new")

    buf = vim.current.buffer
    buf[0] = boardName + " BOARD"
    buf.append("="*( len(boardName)+7 ) )
    buf.append("")
    textWidth = vim.current.window.width

    # Print the issues by category
    for cat in issues:
        buf.append(cat[0].upper()+":")
        buf.append("-"*( len(cat[0])+1 ))
        startLine = len(buf)+1
        i = cat[1]
        endLine = startLine + len(i)-1
        maxKeyLen = 0
        maxSummLen = 0
        for key, summ in i:
            if len(key) >= maxKeyLen:
                maxKeyLen = len(key)
            if len(summ) >= maxSummLen:
                maxSummLen = len(summ)
            buf.append(key + " " + summ)
        vim.command("%d,%dTabularize /\\u\+-\d\+\s/r0l%dr0" % ( startLine, endLine, textWidth-maxKeyLen-maxSummLen-7))
        buf.append("")

    if isinstance(board, KanbanBoard):
        filetype = "jirakanbanboardview"
    else:
        filetype = "jiraboardview"
    vim.command("setl filetype=%s" % filetype)
