Copied from https://gist.github.com/danielestevez/2044589

```bash
# 1) Create a branch with the tag
	git branch {tagname}-branch {tagname}
	git checkout {tagname}-branch

# 2) Include the fix manually if it's just a change .... 
	git add .
	git ci -m "Fix included"
    or cherry-pick the commit, whatever is easier
	git cherry-pick  {num_commit}
	
# 3) Delete and recreate the tag locally
	git tag -d {tagname}
	git tag {tagname}

# 4) Delete and recreate the tag remotely
	git push origin :{tagname} // deletes original remote tag
	git push origin {tagname} // creates new remote tag
		
# 5)  Update local repository with the updated tag (suggestion by @wyattis)
	git fetch --tags
```

This is based on https://gist.github.com/739288 thanks to nickfloyd for it