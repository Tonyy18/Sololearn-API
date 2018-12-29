import requests
from bs4 import BeautifulSoup
import json

exceptions = True

def ex(text):
	if(exceptions):
		raise Exception(text)

class Login():

	def __init__(self, email, password):
		self.loggedIn = False
		self.__loggedIn = False
		if(email and password):
			self.email = email
			self.__password = password
			self.login()
		else:
			ex("Login information is missing")

	def login(self):
		self.__session = requests.Session()
		url = "https://www.sololearn.com/User/Login?ReturnUrl=%2FProfile"
		get = self.__session.get(url)
		if(get.status_code == 200):
			parsed = BeautifulSoup(get.text, "html.parser")
			token = parsed.find("input", {"name": "__RequestVerificationToken"})
			if(token != None):
				token = token.get("value")
				post = self.__session.post(url, data={
					"__RequestVerificationToken": token,
					"Email": self.email,
					"Password": self.__password
				})
				if(post.status_code == 200):
					parsed = BeautifulSoup(post.text, "html.parser")
					name = parsed.find("h1", {"class": "name"})
					if(name != None):
						avatar = parsed.find("div", {"class": "avatar"}).find("img")
						name = avatar.get("alt")
						image = avatar.get("src")
						id = image.split("/")[len(image.split("/")) - 1].split(".")[0]
						self.loggedIn = True
						self.__loggedIn = True
						self.__token = token
						self.name = name
						self.avatar = image
						self.id = id
						details = parsed.find("div", {"class": "detail"}).find_all("div")
						self.level = details[0].text.split("Level")[1].strip()
						self.xp = details[1].find("span").contents[0].split(" ")[0]
						self.profile = User(name, id, avatar, self.__session).profile
					else:
						ex("Login failed")
				else:
					ex("Failed to send login information. Status code " + str(get.status_code))
			else:
				ex("Failed to parse request verification token")
		else:
			ex("Sololearn request failed. Status code " + str(get.status_code))

	def logout(self):
		get = self.__session.get("https://www.sololearn.com/User/Logout")
		if(get.status_code == 200):
			self.loggedIn = False
			self.__loggedIn = False

	def getPosts(self, order = "Trending", page = 1, query = None):
		if(self.__loggedIn):
			orders = ["Trending", "MostRecent", "Unanswered", "MyQuestions", "MyAnswers"]
			if(query == None):
				query = ""
			else:
				query = "&query=" + str(query)
			url = "https://www.sololearn.com/Discuss?page=" + str(page) + query
			for a in orders:
				if(a.lower() == order.lower()):
					url = url + "&ordering=" + a
					break
			re = self.__session.get(url)
			parsed = BeautifulSoup(re.text, "html.parser")
			dic = []
			posts = parsed.find("div", {"id": "questions"})
			if(posts != None):
				posts = posts.find_all("div", {"class": "question"})
				for post in posts:
					dic.append(Post(post, self.id, self.__session))
			return dic
		else:
			ex("User is not logged in")

	def getCodes(self, order = "Trending", page = 1, query = None, language = "all"):
		if(self.__loggedIn):
			url = "https://www.sololearn.com/Codes"
			orders = ["Trending", "MostRecent", "MostPopular", "MyCodes"]
			languages = ["web", "cpp", "c", "cs", "java", "py", "php", "rb", "kt", "swift"]
		
			ordering = ""
			for a in orders:
				if(a.lower() == order.lower()):
					ordering = "?ordering=" + a
					break

			if(query == None):
				query = ""
			else:
				query = "&query=" + str(query)

			lang = ""
			for a in languages:
				if(a.lower() == language.lower()):
					lang = "&language=" + a
					break

			url = url + ordering + lang + query
			try:
				int(page)
				url = url + "&page=" + str(page)
			except:
				url = url
		
			re = self.__session.get(url)
			parsed = BeautifulSoup(re.text, "html.parser")
			publicCodes = parsed.find("div", {"id": "publicCodes"})
			dic = []
			if(publicCodes != None):
				codes = publicCodes.find_all("div", {"class": "codeContainer"})
				for code in codes:
					dic.append(Code(code, self.id, self.__session))
			return dic
		else:
			ex("User is not logged in")

	def getUser(self, id):
		if(self.__loggedIn):
			re = self.__session.get("https://www.sololearn.com/Profile/" + str(id))
			parsed = BeautifulSoup(re.text, "html.parser")
			name = parsed.find("h1", {"class": "name"})
			if(name != None):
				name = name.contents[0].strip()
				avatar = parsed.find("div", {"class": "avatar"}).find("img").get("src")
				return User(name=name, id=id, avatar=avatar, session=self.__session)
		else:
			ex("User is not logged in")

	def newCode(self, name = "Made with API", code = "", cssCode = "", jsCode = "", language=None, public = False):
		if(language != None):
			if(public == True):
				public = "true"
			elif(public == False):
				public = "false"
			editCode(id=0, userId=self.id, language=language, name=name, code=code, cssCode=cssCode, jsCode=jsCode, isPublic=public, session=self.__session)

class Post:

	def __init__(self, post, userId, session):
		self.__post = post
		self.__session = session
		self.__userId = userId
		self.__parse()

	def __parse(self):
		post = self.__post
		stats = post.find("div", {"class": "postStats"})
		votes = stats.find("a", {"class": "postVotes"}).find("p").contents[0]
		ansewers = stats.find("a", {"class": "postAnsewers"}).find("p").contents[0]
		details = post.find("div", {"class": "detailsWrapper"})
		link = details.find("p", {"class": "title"}).find("a")
		title = link.contents[0]
		link = link.get("href")
		id = link.split("/")[2]
		_tags = details.find("div", {"class": "tags"}).find_all("span")
		tags = []
		for tag in _tags:
			tags.append(tag.contents[0])
		author = details.find("a", {"class": "userName"})
		authorId = author.get("href").split("/")[2]
		author = author.contents[0]
		date = details.find("p", {"class": "date"}).contents[0]
		avatar = details.find("a", {"class": "avatar"}).find("img").get("src")
		self.id = id
		self.title = title
		self.link = link
		self.votes = votes
		self.__info() #text
		self.answers = ansewers
		self.tags = tags
		self.date = date
		self.author = User(author, authorId, avatar, self.__session)

	def __info(self):
		re = self.__session.get("https://www.sololearn.com/Discuss/" + self.id)
		parsed = BeautifulSoup(re.text, "html.parser")
		el = parsed.find("div", {"id": "discussionPost"})
		self.text = ""
		if(el != None):
			msg = el.find("p", {"class": "message"})
			if(msg != None):
				if(len(msg.contents) > 0):
					self.text = msg.contents[0]

		self.currentVote = "0"
		voted = el.find("div", {"class": "upVote"})
		if(voted != None and "active" in voted.get("class")):
			self.currentVote = "1"
		else:
			voted = el.find("div", {"class": "downVote "})
			if(voted != None and "active" in voted.get("class")):
				self.currentVote = "-1"

	def getAnswers(self, index = 0, order = "Votes"):
		orderings = ["Votes", "Date"]
		for a in orderings:
			if(order.lower() == a.lower()):
				order = a
				break
		re = self.__session.post("https://www.sololearn.com/Discuss/GetReplies", data={
			"postId": self.id,
			"index": str(index),
			"questionAuthorId": self.author.id,
			"ordering": a
		})
		text = json.loads(re.text)["html"]
		parsed = BeautifulSoup(text, "html.parser")
		dic = []
		answers = parsed.find_all("div", {"class": "answer"})
		for answer in answers:
			dic.append(Answer(answer, self.__session))
		return dic

	def sendAnswer(self, text):
		self.__session.post("https://www.sololearn.com/Discuss/Reply", data={
			"parentId": self.id,
			"message": str(text),
			"questionAuthorId": self.author.id
		})

	def edit(self, title = None, text = None, tags = None):
		if(title == None):
			title = self.title
		if(text == None):
			text = self.text
		if(tags == None):
			tags = self.tags
		url = "https://www.sololearn.com/Discuss/Edit/" + self.id
		re = self.__session.post(url, data={
			"id": self.id,
			"ParentId": "",
			"UserId": self.__userId,
			"Title": title,
			"Message": text,
			"TagsSingleField": ",".join(tags)
		})

	def delete(self):
		deletePost(self.id, self.__session)

	def vote(self, amount):
		votePost(amount, self.id, self.__session)

	def json(self):
		return {
			"id": self.id,
			"title": self.title,
			"link": self.link,
			"votes": self.votes,
			"answers": self.answers,
			"tags": self.tags,
			"date": self.date,
			"author": self.author.json()
		}

	def __str__(self):
		return json.dumps(self.json())

class User:

	def __init__(self, name, id, avatar, session):
		self.name = name
		self.id = id
		self.avatar = avatar
		self.__session = session
		self.__profileBool = False

	def profile(self):
		re = self.__session.get("https://www.sololearn.com/Profile/" + str(self.id))
		parsed = BeautifulSoup(re.text, "html.parser")
		profile = Profile(parsed, self.id, self.__session)
		self.__profileBool = True
		self.__profile = profile
		self.name = profile.name
		self.id = profile.id
		self.avatar = profile.avatar
		return profile

	def json(self):
		if(self.__profileBool):
			return self.__profile.json()
		return {
			"id": self.id,
			"name": self.name,
			"avatar": self.avatar
		}

	def __str__(self):
		return json.dumps(self.json())

class Answer:

	def __init__(self, answer, session):
		self.__answer = answer,
		self.__session = session
		self.__parse()

	def __parse(self):
		answer = self.__answer[0] #Tuple
		id = answer.get("data-id")
		votes = answer.get("data-votes")
		state = answer.get("data-state")
		voted = answer.find("div", {"class": "upVote"})
		if(voted != None and "active" in voted.get("class")):
			voted = "1"
		else:
			voted = answer.find("div", {"class": "downVote"})
			if(voted != None and "active" in voted.get("class")):
				voted = "-1"
			else:
				voted = "0"
		message = answer.find("p", {"class": "message"})
		text = ""
		if(message != None and len(message.contents) > 0):
			text = message.contents[0]

		date = answer.find("p", {"class": "date"})
		date = date.get("data-date")

		a = answer.find("a", {"class": "userName"})
		author = a.contents[0]
		authorId = a.get("href").split("/")[2]
		avatar = answer.find("a", {"class": "avatar"})
		avatar = avatar.find("img")
		avatar = avatar.get("src")

		self.id = id
		self.votes = votes
		self.currentVote = voted
		self.state = state
		self.text = text
		self.date = date
		self.author = User(author, authorId, avatar, self.__session)

	def edit(self, text):
		re = self.__session.post("https://www.sololearn.com/Discuss/EditPost", data={
			"id": self.id,
			"message": text
		})

	def vote(self, amount):
		votePost(amount, self.id, self.__session)

	def delete(self):
		deletePost(self.id, self.__session)

	def json(self):
		return {
			"id": self.id,
			"votes": self.votes,
			"currentVote": self.currentVote,
			"state": self.state,
			"text": self.text,
			"date": self.date,
			"author": self.author.json()
		}

	def __str__(self):
		return json.dumps(self.json())

class Code:

	def __init__(self, code, userId, session):
		self.__code = code
		self.__userId = userId
		self.__session = session
		self.__parse()

	def __parse(self):
		code = self.__code
		id = code.get("data-id")
		a = code.find("a", {"class": "icon"})
		language = a.contents[0]
		link = a.get("href")
		name = code.find("a", {"class": "nameLink"}).contents
		if(len(name) > 0):
			name = name[0]
		else:
			name = ""
		voted = code.find("div", {"class": "upvote"})
		currentVote = "0"
		if(voted != None and "active" in voted.get("class")):
			currentVote = "1"
		else:
			voted = code.find("div", {"class": "downvode"})
			if(voted != None and "active" in voted.get("class")):
				currentVote = "-1"
		votes = code.find("div", {"class": "vote"})
		votes = votes.find("p")
		votes = votes.contents[0]
		if("+" in votes):
			votes = votes[1::]
		a = code.find("a", {"class": "userName"})
		if(a != None):
			author = a.contents[0]
			authorId = a.get("href").split("/")[2]
			avatar = code.find("a", {"class": "avatar"}).find("img").get("src")
		date = code.find("p", {"class": "codeDate"})
		date = date.contents[0]
		self.id = id
		self.publicId = link.split("/")[3]
		self.language = language
		self.link = link
		self.name = name
		self.currentVote = currentVote
		self.votes = votes
		self.date = date
		if(a != None):
			self.author = User(author, authorId, avatar, self.__session)

	def vote(self, amount):
		amount = int(amount)
		if(amount > 1):
			amount = 1
		elif(amount < -1):
			amount = -1
		re = self.__session.post("https://www.sololearn.com/UserCodes/CodeVoting/", data={
			"codeId": str(self.id),
			"vote": str(amount)
		})		

	def source(self):
		re = self.__session.get(self.link)
		parsed = BeautifulSoup(re.text, "html.parser")
		form = parsed.find("form", {"id": "saveForm"})
		code = form.find("input", {"id": "Code"}).get("value")
		cssCode = form.find("input", {"id": "CssCode"}).get("value")
		jsCode = form.find("input", {"id": "JsCode"}).get("value")
		return {
			"code": code,
			"cssCode": cssCode,
			"jsCode": jsCode
		}

	def edit(self, name = None, code = None, cssCode = None, jsCode = None, public = True, language = None):
		if(name == None):
			name = self.name
		if(code == None or cssCode == None or jsCode == None):
			sc = self.source()
			if(code == None):
				code = sc["code"]
			if(cssCode == None):
				cssCode = sc["cssCode"]
			if(jsCode == None):
				jsCode = sc["jsCode"]
		if(public == True):
			public = "true"
		elif(public == False):
			public = "false"
		if(language == None):
			language = self.language
		editCode(id=self.id, userId=self.__userId, language=language, name=name, code=code, cssCode=cssCode, jsCode=jsCode, publicId=self.publicId, isPublic=public, session=self.__session)
	
	def delete(self):
		re = self.__session.post("https://www.sololearn.com/UserCodes/RemoveUserCode/", data={
			"codeId": self.id,
			"userId": self.__userId
		})

	def execute(self):
		if(self.language != "web"):
			source = self.source()["code"]
			re = self.__session.post("https://code.sololearn.com/RunCode/", data={
				"sourceCode": source,
				"language": self.language,
				"parameters": ""
			})
			return json.loads(re.text)["output"]

	def json(self):
		return {
			"id": self.id,
			"publicId": self.publicId,
			"language": self.language,
			"link": self.link,
			"name": self.name,
			"currentVote": self.currentVote,
			"votes": self.votes,
			"date": self.date,
			"author": self.author.json()
		}

	def __str__(self):
		return json.dumps(self.json())

class Profile:
	def __init__(self, parsed, id, session):
		self.__parsed = parsed
		self.__session = session
		self.__parse()
		self.id = id

	def __parse(self):
		parsed = self.__parsed
		name = parsed.find("h1", {"class": "name"})
		if(name != None):
			name = name.contents[0].strip()
			avatar = parsed.find("div", {"class": "avatar"}).find("img").get("src")
			id = avatar.split("/")[len(avatar.split("/")) - 1].split(".")[0]
			details = parsed.find("div", {"class": "detail"})
			details = details.find_all("div")
			level = details[0]
			level = level.contents[2].strip()
			xp = details[1]
			xp = xp.find("span").contents[0].split(" ")[0]
			self.id = id
			self.name = name
			self.avatar = avatar
			self.level = level
			self.xp = xp
			self.__courses()
			self.__codes()
			self.__certs()
			self.__achies()

	def __courses(self):
		parsed = self.__parsed
		userCourses = parsed.find("div", {"class": "userCourses"})
		self.courses = []
		if(userCourses != None):
			userCourses = userCourses.find_all("div", {"class": "courseWrapper"})
			for course in userCourses:
				percent = course.find("div", {"class": "chart"}).get("data-percent")
				courseXp = course.find("p", {"class": "courseXp"}).contents[0].split(" ")[0]
				course = course.find("a", {"class": "course"})
				title = course.get("title")
				icon = course.find("img").get("src")
				name = course.get("href").split("/")[len(course.get("href").split("/")) - 1]
				self.courses.append({
					"name": name,
					"title": title,
					"percent": percent,
					"xp": courseXp,
					"icon": icon
				})

	def __codes(self):
		parsed = self.__parsed
		codes = parsed.find("div", {"id": "userCodes"})
		self.codes = []
		if(codes != None):
			codes = codes.find_all("div", {"class": "codeContainer"})
			for code in codes:
				self.codes.append(Code(code, self.id, self.__session))

	def __certs(self):
		parsed = self.__parsed
		certs = parsed.find("div", {"id": "certificates"})
		self.certificates = []
		if(certs != None):
			certs = certs.find_all("div", {"class": "certificate"})
			for cert in certs:
				title = cert.get("title")
				name = cert.get("data-alias")
				self.certificates.append({
					"name": name,
					"title": title
				})

	def __achies(self):
		parsed = self.__parsed
		achievements = parsed.find("div", {"class": "userAchievements"})
		self.achievements = []
		if(achievements != None):
			achievements = achievements.find_all("div", {"class": "achievement"})
			for ach in achievements:
				title = ach.get("title")
				disabled = False
				if("disabled" in ach.get("class")):
					disabled = True
				icon = ach.find("div", {"class": "icon"}).find("img").get("src")
				desc = ach.find("div", {"class": "description"}).contents[0].strip()
				self.achievements.append({
					"title": title,
					"desc": desc,
					"icon": icon,
					"disabled": disabled
				})

	def json(self):
		return {
			"id": self.id,
			"name": self.name,
			"avatar": self.avatar,
			"level": self.level,
			"xp": self.xp,
			"courses": self.courses,
			"codes": self.codes,
			"certificates": self.certificates,
			"achievements": self.achievements
		}

	def __str__(self):
		return json.dumps(self.json())

def votePost(amount, id, session):
	amount = int(amount)
	if(amount > 1):
		amount = 1
	elif(amount < -1):
		amount = -1
	re = session.post("https://www.sololearn.com/Discuss/VotePost/", data={
		"postId": str(id),
		"vote": str(amount)
	})

def deletePost(id, session):
	session.post("https://www.sololearn.com/Discuss/DeletePost", data={
		"postId": str(id)
	})

def editCode(id = 0, userId = None, language = None, name = None, code = "", cssCode = "", jsCode = "", publicId = None, isPublic = "false", session = None):
	data = {
		"id": str(id),
		"userId": userId,
		"language": language,
		"name": name,
		"sourceCode": code,
		"cssCode": cssCode,
		"jsCode": jsCode,
		"isPublic": isPublic
	}
	if(publicId != None):
		data["publicId"] = publicId
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
	}
	re = session.post("https://code.sololearn.com/EditCode/", data=data, headers=headers)