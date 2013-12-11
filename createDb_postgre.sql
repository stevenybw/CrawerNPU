DROP TABLE URL;
DROP TABLE Content;
CREATE TABLE Content(
sha1	bytea,
content	varchar(500000),
CONSTRAINT content_pk PRIMARY KEY(sha1));

CREATE TABLE URL(
url		char(200),
content		bytea	not null,
stamp_fetched	timestamp	not null,
CONSTRAINT url_pk PRIMARY KEY(url),
CONSTRAINT url_fk FOREIGN KEY(content)
	REFERENCES Content(sha1)
	ON DELETE CASCADE);