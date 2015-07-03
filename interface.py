# Interface for The Number Graph.
# Initial IDs:
# Thread:  2dwxho
# Comment: cju11n6
import praw

# PRAW Initialisation
r = praw.Reddit(user_agent='the-number-graph by /u/glider97')

f1 = open("latest.txt", 'r')    # latest.txt stores the ids of the last comment and thread used.
latest = f1.read().split('\n')  # They are stored in a list called 'latest'
f1.close()                      # 'details.txt' stores a log of all the comments "approved".
f2 = open("details.txt", "a+")  #

# latest.txt Legend:
#	0 - curThreadID
#	1 - curComID

curThreadID=latest[0] # ID of the Number Thread
curComID=latest[1] # First comment's ID in the Number Thread.
comms=[] # List of comments saved.

f2.write("========================================================\n")
f2.write(str(curThreadID)+'\n') # Log ID of thread about to be used. Buggy.

def main():
	# Begin.
	start()

def migrate():
	# The function of migrate() is to change the thread ID
	# (and consequently the comment ID) on which the work is to be done.
	# See: last comment of The Mona Lisa Thread.

	global curThreadID
	global curComID
	global comms
	curThreadID=raw_input("Enter the Thread ID (ex: 2dwxho):")
	curComID=raw_input("Enter the Comment ID (ex: cju11n6):")

	try:
		thread = r.get_submission('http://www.reddit.com/r/explainlikeimfive/comments/' + curThreadID + "/_/" + curComID)
	except Exception,e:
		print "Error! Please try again."
		print e
	else:
		curComID = thread.comments[0] # Make comment ID variable as comment object.
		postTime = datetime.fromtimestamp(int(curComID.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
		comms.append([curComID.id, curComID.author, postTime, curComID.body]) # Append a list of data of the comment.
	if type(curComID)==str: # If thread or comment not found.... Maybe useless?
		curComID, curThreadID=''
		comms=[]
		print "Comment not found. Please try again."
		main() # Reset and try again.

def start():
	# The core of the script. Gives an interface to 'store', 'discard', or
	# 'save' a comment, and to 'migrate' to another thread.

	global curThreadID
	global curComID
	global comms
	char = ''
	temp = [] # Store the comment data. Later add to comms list.
	if curComID=='' or curThreadID=='': # If thread or comment ID not found in latest.txt....
		migrate()                       # go to migrate() and get it.
	elif type(curComID)==str:
		thread = r.get_submission('http://www.reddit.com/r/explainlikeimfive/comments/' + curThreadID + "/_/" + curComID)
		curComID = thread.comments[0]
		postTime = datetime.fromtimestamp(int(curComID.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
		comms.append([curComID.id, curComID.author, postTime, curComID.body]) # Append a list of data of the comment.
	if len(curComID.replies)==0:
		print "This is the latest comment yet."
	else:
		# Interface begins.

		char = 0
		x = 0
		while x < len(curComID.replies):
			y = curComID.replies[x]
			if type(y)==praw.objects.MoreComments: # "load more comments"
				y = y.comments()[0]
			postTime = datetime.fromtimestamp(int(y.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
			print "Comment made by", y.author, 'at', postTime
			print '"' + y.body + '"'
			char = raw_input("1)Store     2)Discard     3)Store, Save and Migrate     4)Save     5)Exit\n")
			if char=='1':
				temp.append([y.id, y.author, postTime, y.body]) # "Approve" the comment. 'Save' later.
				curComID = y
				x=0
			elif char=='2':
				x+=1 # Disapprove/Discard the current comment.
			elif char=='3':
				for i in temp:
					comms.append(i)
				temp=[]
				x=0
				migrate() # "Approve", 'save' and move on to another thread.
			elif char=='4':
				for i in temp:      # A code snippet....
					comms.append(i) # to 'save' the comments "approved".
				temp=[]
			elif char=='5':
				break
		if char != '3' and char!='5': # Bugs???
			print "The thread has come to an end. This was the latest comment."
			char = raw_input("Progress Saved!\nDo you want to (m)igrate to a new thread, or (s)top?")
			for i in temp:
				comms.append(i) # 'Save'
			if char=='m':
				migrate()
				main()

		# Interface ends.
	for i in comms:
		if i == ['','','','']: # Remove empty comment data, if any. Maybe useless?
			comms.remove(i)
	f1 = open("latest.txt", 'w')                          # Write the last thread and comment
	f1.write(str(curThreadID)+'\n'+str(curComID.id)+'\n') # IDs operated upon.
	f1.close()
	for i in comms:
		f2.write(str(i[0])+'\n') # Log the comment IDs "approved".
	f2.close()
	# Placeholder to either return list to 'plot' script....
	# or call the script itself by parameters.


if __name__=='__main__':
	main()
