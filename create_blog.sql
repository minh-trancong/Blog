USE blog;
CREATE TABLE `User` (
  `userid` INT PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(255) UNIQUE NOT NULL,
  `username` varchar(255)  UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `firstname` nvarchar(255),
  `lastname` nvarchar(255),
  `occupation` nvarchar(255),
  `phone` CHAR(10),
  `status` char(10),
  `picture_url` varchar(1000)
);


CREATE TABLE `Post` (
  `postid` INT PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(1000),
  `body` varchar(8000),
  `timestamp` DATETIME,
  `userid` INT,
  CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES User(userid)
);

CREATE TABLE `React` (
  `postid` INT,
  `userid` INT,
   CONSTRAINT PK_react PRIMARY KEY (postid, userid),
   CONSTRAINT FK_postid FOREIGN KEY (postid) REFERENCES Post(postid),
   CONSTRAINT FK_react_userid FOREIGN KEY (userid) REFERENCES User(userid)
);