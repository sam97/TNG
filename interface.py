# Interface for The Number Graph.
# Initial IDs:
# Thread:  2dwxho
# Comment: cju11n6
import praw

# PRAW Initialisation
r = praw.Reddit(user_agent='the-number-graph by /u/glider97')

f1 = open("latest.txt", 'r')
latest = f1.read().split('\n')
f1.close()
f2 = open("details.txt", "a+")

# File Legend:
#	0 - curThreadID
#	1 - curComID
#	2 - Array of comments (feature abolished)

curThreadID=latest[0] # ID of the Number Thread
curComID=latest[1] # First comment's ID in the Number Thread.
comms=[] # List of comments saved.

f2.write("========================================================\n")
f2.write(str(curThreadID)+'\n')
# for i in range(2,len(details)-1,4):
# 	comms.append([])
# 	for j in range(0,4):
# 		comms[i-2].append(details[i+j]) ###
# comms = details[2]

def main():
	# print """
	# Welcome. Let's begin.
	# The options available are:
	# 1. Start/Next
	# 2. Stop
	# 3. Migrate
	# Enter your choice:
	# """
	# ch=raw_input()
	# while (ch!='n'):
	# 	if ch==1:
	# 		start()
	# 	elif ch==2:
	# 		stop()
	# 	elif ch==3:
	# 		migrate()
	# 	ch=raw_input()
	start()

def migrate():
	global curThreadID
	global curComID
	global comms
	curThreadID=raw_input("Enter the Thread ID:")
	# thread = r.get_submission(submission_id=curThreadID)
	# curThreadID = thread
	# thread = praw.helpers.flatten_tree(thread.comments)
	curComID=raw_input("Enter the Comment ID:")
	# for i in range(0,len(thread)):
	# 	if thread[i].id == curComID:
	# 		curComID = thread[i]
	# 		postTime = datetime.fromtimestamp(int(curComID.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
	# 		# print "Comment found at", curComID
	# 		comms.append([curComID.id, curComID.author, postTime, curComID.body])
	# 		break
	try:
		thread = r.get_submission('http://www.reddit.com/r/explainlikeimfive/comments/' + curThreadID + "/_/" + curComID)
	except Exception,e:
		print "Comment not found. Please try again."
		print e
	else:
		curComID = thread.comments[0]
		postTime = datetime.fromtimestamp(int(curComID.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
		comms.append([curComID.id, curComID.author, postTime, curComID.body])
	if type(curComID)==str:
		curComID, curThreadID=''
		comms=[]
		print "Comment not found. Please try again."
		main()

def start():
	global curThreadID
	global curComID
	global comms
	char = ''
	temp = []
	if curComID=='' or curThreadID=='':
		migrate()
	elif type(curComID)==str:
		thread = r.get_submission('http://www.reddit.com/r/explainlikeimfive/comments/' + curThreadID + "/_/" + curComID)
		curComID = thread.comments[0]
		postTime = datetime.fromtimestamp(int(curComID.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
		comms.append([curComID.id, curComID.author, postTime, curComID.body])
	# while char!=4:
	if len(curComID.replies)==0:
		print "This is the latest comment yet."
	else:
		char = 0
		x = 0
		# for x in curComID.replies:
		# def enlist(id):
		# 	commsList = []
		# 	commsList.append(id.replies[0])
		# 	if len(id.replies) > 1:
		# 		for i in id.replies[1].comments():
		# 			commsList.append(i)
		# 	return commsList
		# commsList = enlist(curComID)
		while x < len(curComID.replies):
			y = curComID.replies[x] # extra added
			# print "DEBUG FLAG"
			if type(y)==praw.objects.MoreComments:
				y = y.comments()[0]
				# curComID = y.comments()[0]
				# x=0
				# continue
			# print "DEBUG FLAG: type of curComID.replies(x) is", type(y), type(curComID.replies), type(curComID)
			postTime = datetime.fromtimestamp(int(y.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
			print "Comment made by", y.author, 'at', postTime
			print '"' + y.body + '"'
			char = raw_input("1)Store     2)Discard     3)Store, Save and Migrate     4)Save     5)Exit\n")
			if char=='1':
				temp.append([y.id, y.author, postTime, y.body])
				curComID = y
				# commsList = enlist(curComID)
				x=0
			elif char=='2':
				x+=1
			elif char=='3':
				for i in temp:
					comms.append(i)
				temp=[]
				x=0
				migrate()
				# commsList = enlist(curComID)
			elif char=='4':
				for i in temp:
					comms.append(i)
				temp=[]
				# curComID = y
			elif char=='5':
				break
			# x+=1
		if char != '3' and char!='5':
			print "The thread has come to an end. This was the latest comment."
			char = raw_input("Progress Saved!\nDo you want to (m)igrate to a new thread, or (s)top?")
			for i in temp:
				comms.append(i)
			if char=='m':
				migrate()
				main()
	for i in comms:
		if i == ['','','','']:
			comms.remove(i)
	# f.seek(0,0)
	f1 = open("latest.txt", 'w')
	f1.write(str(curThreadID)+'\n'+str(curComID.id)+'\n')
	f1.close()
	for i in comms:
		f2.write(str(i[0])+'\n')
	f2.close()


if __name__=='__main__':
	main()
