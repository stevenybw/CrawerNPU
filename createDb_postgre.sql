DROP TABLE URL;
DROP TABLE Content;
DROP TABLE tocrawl;
CREATE TABLE Content(
sha1	bytea,
content	varchar(500000),
CONSTRAINT content_pk PRIMARY KEY(sha1));

CREATE TABLE URL(
url		varchar(500),
content		bytea	not null,
stamp_fetched	timestamp	not null,
CONSTRAINT url_pk PRIMARY KEY(url),
CONSTRAINT url_fk FOREIGN KEY(content)
	REFERENCES Content(sha1)
	ON DELETE CASCADE);
	
CREATE TABLE tocrawl(
id		int,
url		varchar(500),
CONSTRAINT tocrawl_pk PRIMARY KEY(id)
);

GRANT ALL ON Content, URL, tocrawl TO python;
