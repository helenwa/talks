git log --pretty=format:"[%h] %aN %ad %s" --date=short --numstat --after=2015-01-01 -- . ":(exclude)**/test/**" ":(exclude)**/pom.xml" --grep=" fix " > git_log.log
java -jar {PATH}/code-maat-1.1.jar -l git_log _no_tests.log -c git > {PATH}/code_churn.csv
