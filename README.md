# Sololearn API Unofficial

<p>Sololearn API for python.</p>
<h2>Login system needs to be updated!! Not working otherwise</h2>
<h3>The script is outdated and propably requires javascript. Will be converted into selenium at some point</h3>
<p>Requires <a href="http://docs.python-requests.org/en/master/">requests</a>, <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">BeautifulSoup 4</a> and <a href="https://docs.python.org/2/library/json.html">json</a> libraries</p>

<h1>Documentation</h1>
<div id="login">
<h1>Login</h1>
<p>Before you can use this API you must login with your sololearn account</p>

```python
import sl
login = sl.Login("email", "password")
```
<p>Login instance contains following properties</p>
<ul>
  <li>loggedIn</li>
  <li>id</li>
  <li>name</li>
  <li>avatar</li>
  <li>level</li>
  <li>xp</li>
  <li><a href="#profile">profile</a></li>
  <li><a href="#getPosts">getPosts</a></li>
  <li><a href="#getCodes">getCodes</a></li>
  <li><a href="#getUser">getUser</a></li>
  <li><a href="#newCode">newCode</a></li>
</ul>
<div id="getPosts">
  <h2>getPosts</h2>
  <p>Returns a list of <a href="#post">Post</a> objects</p>
  <b>Parameters</b>
  <ul>
    <li><b>order</b> Trending, MostRecent, Unanswered, MyQuestions, MyAnswers. Trending is the default value</li>
    <li><b>page</b> Each page returns 20 posts</li>
    <li><b>query</b> Keyword used to search posts</li>
  </ul>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  posts = login.getPosts(order="myquestions", page=2)
  ```
  <p>More information in <a href="#post">Post</a> object section</p>
</div>
<div id="getCodes">
  <h2>getCodes</h1>
  <p>Returns a list of <a href="#code">Code</a> objects</p>
  <b>Parameters</b>
  <ul>
    <li><b>order</b> Trending, MostRecent, MostPopular, MyCodes</li>
    <li><b>page</b> Each page has 20 codes</li>
    <li><b>query</b> Keyword used to search codes</li>
    <li><b>language</b> Codes by specific language. Must be used with the alias of the language. Listed below. Searches all languages by default</li>
  </ul>
  <b>Language aliases</b>
  <p>web, cpp, c, cs, java, py, php, rb, kt, swift</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  codes = login.getCodes(query="website", language="web")
  ```
  More information in <a href="#code">Code</a> object section

</div>
<div id="getUser">
  <h2>getUser</h2>
  <p>Returns <a href="#user">User</a> object for given user id</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  user = login.getUser(7745624)
  print(user.name)
  print(user.level + " " + user.xp)
  ```
  More information in <a href="#user">User</a> object section
</div>
<div id="newCode">
  <h2>newCode</h2>
  <p>Creates and saves a new code for your user</p>
  <b>Parameters</b>
  <ul>
    <li><b>name</b></li>
    <li><b>code</b> source code</li>
    <li><b>cssCode</b> only used with web language to specify source code for css</li>
    <li><b>jsCode</b> only used with web language to specify source code for javascript</li>
    <li><b>language</b> Required. Must be used with the alias of the language. Listed below</li>
    <li><b>public</b> boolean</li>
  </ul>
  <b>Language aliases</b>
  <p>web, cpp, c, cs, java, py, php, rb, kt, swift</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  login.newCode(language="py", name="Python code", code="print('hello world')", public=True)
  login.newCode(language="web", name="Web code", code="html code", cssCode="css code", jsCode="javascript code", public=False)
  ```
</div>
</div>
<div id="#post">
  <h1>Post</h1>
  <p>Post object contains information for a single post</p>
  <p>It contains following properties</p>
  <ul>
    <li>id</li>
    <li>title</li>
    <li>link</li>
    <li>votes</li>
    <li>currentVote</li>
    <li>text</li>
    <li>answers</li>
    <li>tags</li>
    <li>date</li>
    <li>author (<a href="#user">User</a> object)</li>
    <li><a href="#getAnswers">getAnswers</a></li>
    <li><a href="#sendAnswer">sendAnswer</a></li>
    <li><a href="#editPost">edit</a></li>
    <li><a href="#delete">delete</a></li>
    <li><a href="#vote">vote</a></li>
    <li><a href="#json">json</a></li>
  </ul>
  <div id="getAnswers">
    <h2>getAnswers</h2>
    <p>Returns a list of <a href="#answer">Answer</a> objects</p>
    <b>Parameters</b>
    <ul>
      <li><b>index</b> starting index. Returns 20 answers starting from the index</li>
      <li><b>order</b> get answers by votes or date</li>
    </ul>
    
  ```python
  import sl
  login = sl.Login("email", "password")
  posts = login.getPosts()
  answers = posts[0].getAnswers(order="date", index=100)
  ```
   <p>More information in <a href="#answer">Answer</a> object section</p>
  </div>
  <div id="sendAnswer">
    <h2>sendAnswer</h2>
    <p>Sends an answer to the parent <a href="#post">Post</a> object</p>
    <b>Parameters</b>
    <ul>
      <li><b>text</b> text for the answer</li>
    </ul>
  </div>
  <div id="editPost">
    <h2>edit</h2>
    <p>(<a href="#post">Post</a> object)</p>
    <b>Parameters</b>
    <ul>
      <li><b>title</b></li>
      <li><b>text</b></li>
      <li><b>tags</b> (list)</li>
    </ul>
    <p>Only possible for your own posts/questions</p>
    <p>If parameter is not used it will keep its original content</p>
    
  ```python
  import sl
  login = sl.Login("email, "password")
  posts = login.getPosts(order="myquestions")
  posts[0].edit(title="answer title", text="answer body", tags=["tag1", "tag2"])
  ```
  </div>
</div>
<div id="user">
  <h1>User</h1>
  <p>Is used to store information for user</p>
  <ul>
    <li>id</li>
    <li>name</li>
    <li>avatar</li>
    <li><a href="#profile">profile</a></li>
    <li><a href="#json">json</a></li>
  </ul>
  <div id="profile">
    <h2>profile</h2>
    <p>This method is used to get more specific information about the user</p>
    <p>Returns <a href="#profileObject">Profile</a> object</p>
    <p>This method takes no parameters</p>
  </div>
</div>
<div id="profileObject">
  <h1>Profile</h1>
  <p>Retrieves more specific information for user</p>
  <p>Only callable from <a href="#user">User</a> object</p>
  <p>It contains following properties</p>
  <ul>
    <li>id</li>
    <li>name</li>
    <li>avatar</li>
    <li>level</li>
    <li>xp</li>
    <li>courses (dictionary)</li>
    <li>codes (list of <a href="#code">Code</a> objects)</li>
    <li>certificates (dictionary)</li>
    <li>achievements (dictionary)</li>
  </ul>
  <p>Parent object properties are synchronized along with the <a href="#profileObject">Profile</a> object properties</p>
</div>
<div id="answer">
  <h1>Answer</h1>
  <p>Answer object contains information for a single answer</p>
  <p>Answer objects are returned from <a href="#getAnswers">getAnswers</a> method in <a href="#post">Post</a> object</p>
  <p>It contains following properties</p>
  <ul>
    <li>id</li>
    <li>votes</li>
    <li>currentVote</li>
    <li>state</li>
    <li>text</li>
    <li>date</li>
    <li>author (<a href="#user">User</a> object)</li>
    <li><a href="#editAnswer">edit</a></li>
    <li><a href="#delete">delete</a></li>
    <li><a href="#vote">vote</a></li>
    <li><a href="#json">json</a></li>
  </ul>
  <div id="editAnswer">
    <h2>edit</h2>
    <p>(<a href="#answer">Answer</a> object)</p>
    <p>Takes a single string as parameter</p>
    <p>Only possible for your own answers</p>
    
  ```python
  import sl
  login = sl.Login("email", "password")
  posts = login.getPosts()
  answers = posts[0].getAnswers(order="date", index=100)
  answers[0].edit("edited")
  ```
  </div>
</div>
<div id="code">
  <h1>Code</h1>
  <p>Post object contains information for a single post</p>
  <p>It contains following properties</p>
  <ul>
    <li>id</li>
    <li>publicId</li>
    <li>language</li>
    <li>link</li>
    <li>name</li>
    <li>votes</li>
    <li>currentVote</li>
    <li>date</li>
    <li>author (<a href="#user">User</a> object)</li>
    <li><a href="#source">source</a></li>
    <li><a href="#editCode">edit</a></li>
    <li><a href="#execute">execute</a></li>
    <li><a href="#vote">vote</a></li>
    <li><a href="#delete">delete</a></li>
    <li><a href="#json">json</a></li>
  </ul>
  <div id="source">
    <h2>source</h2>
    <p>Returns dictionary including source code for <a href="#code">Code</a> object</p>
    <b>Values</b>
    <ul>
      <li><b>code</b> the actual source code. Contains html source code when using web language</li>
      <li><b>cssCode</b> Contains source code for css language. only used with web language. Otherwise empty</li>
      <li><b>jsCode</b> Contains source code for javascript language. only used with web language. Otherwise empty</li>
    </ul>
    
  ```python
  import sl
  login = sl.Login("email", "password")
  codes = login.getCodes()
  source = codes[0].source()
  print(source["code"])
  ```
  </div>
  <div id="editCode">
    <h2>edit</h2>
    <p>(<a href="#">Code</a> object)</p>
    <b>Parameters</b>
    <ul>
      <li><b>name</b></li>
      <li><b>code</b> source code</li>
      <li><b>cssCode</b> only used when editing code with web language</li>
      <li><b>jsCode</b> only used when editing code with web language</li>
      <li><b>language</b> Keeps the original language by default. Must be used with the alias of the language. Listed below</li>
      <li><b>public</b></li>
    </ul>
    <p>Only possible for your own codes</p>
    <b>Language aliases</b>
    <p>web, cpp, c, cs, java, py, php, rb, kt, swift</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  codes = login.getCodes()
  codes[0].edit(name="Edited", code="print('edited')", public=False)
  ```
  </div>
  <div id="execute">
    <h2>execute</h2>
    <p>Executes the code and returns the output</p>
    <p>Doesn't work with web language</p>
    
  ```python
  import sl
  login = sl.Login("email", "password")
  login.newCode(language="py", code="print('Hello World')")
  codes = login.profile().codes
  print(codes[0].execute())
  ```
  </div>
</div>
<div id="delete">
  <h2>delete</h2>
  <p>This method is property of <a href="#post">Post</a>, <a href="#answer">Answer</a> and <a href="#code">Code</a> objects</p>
  <p>Deletes the object</p>
  <p>This method takes no parameters</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  posts = login.getPosts(order="myquestions")
  codes = login.getCodes(order="mycodes")
  answers = posts[0].getAnswers()
  posts[0].delete()
  codes[0].delete()
  if(answers[0].author.id == login.id):
      answers[0].delete()
  ```
</div>
<div id="vote">
  <h2>vote</h2>
  <p>This method is property of <a href="#post">Post</a>, <a href="#answer">Answer</a> and <a href="#code">Code</a> objects</p>
  <p>Sends a vote to the parent object</p>
  <b>parameters</b>
  <ul>
    <li><b>amount</b> values 1, 0 and -1</li>
  </ul>
  <p>value 1 upvotes</p>
  <p>value 0 removes upvote or downvote</p>
  <p>value -1 downvotes</p>
  
  ```python
  import sl
  login = sl.Login("email", "password")
  posts = login.getPosts()
  codes = login.getCodes()
  answers = posts[0].getAnswers()
  posts[0].vote(1)
  codes[0].vote(0)
  answers[0].vote(-1)
  
  ```
</div>
<div id="json">
  <h2>json</h2>
  <p>Returns json data from the parent object<p>
  <p>Exists in every object</p>
</div>
<h1>Examples</h1>
<h2>Delete all your questions/codes</h2>

```python
import sl
login = sl.Login("email", "password")
questions = login.getPosts(order="myquestions")
for question in questions:
    question.delete()
```
<h2>User info for trending codes</h2>

```python
import sl
login = sl.Login("email", "password")
codes = login.getCodes()
for code in codes:
    print(code.author.id)
    print(code.author.name)
    print(code.author.avatar)
```
<h2>Create new code and execute it</h2>

```python
import sl
login = sl.Login("email", "password")
login.newCode(language="py", name="new code", code="print('Hello World')")
codes = login.profile().codes
print(codes[0].execute())
```
