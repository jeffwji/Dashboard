pipeline {
    /**
     * Jenkins 选项和运行时选项
     */
    agent {         // any
      node {        // 可选
        label "Python3"
      }
    }

    options{
      timestamps()
      disableConcurrentBuilds()             // 禁止并行，每次只允许一个构建。
      timeout(time: 30, unit: 'MINUTES')    // java.util.concurrent.TimeUnit
    }

    /**
     * 自定义环境变量
     */
    environment {
        GIT_URL       = 'git@github.com:jeffwji/Dashboard.git'
        CREDENTIAL    = 'Github'
        BRANCH        = 'develop'
        PYPI_CREDENTIAL = "PypiRepo"
    }

    /**
     * 编译过程由多个 Stage(阶段)构成.
     */
    stages {
        /**
         * 每个阶段下可再分 step
         */
        stage('Clear up workspace') {
            steps {
                // 打印环境变量
                sh 'printenv'

                // 清理缓存缓存
                echo "Delete workspace ${workspace}"

                dir("${workspace}") {
                    deleteDir()
                }
                dir("${workspace}@tmp") {
                    deleteDir()
                }
            }
        }

        /**
         * Dload source code
         */
        stage('Get code from Github') {
            steps {
                script{     // Java script
                  println('Get code from Github')   // println 等效于 echo
                }
                git branch: "${env.BRANCH}", credentialsId: "${env.CREDENTIAL}", url: "${env.GIT_URL}"   // 使用 env 名称空间下的环境变量
            }
        }

        /**
         * Install dependency for coverage and unittest(nosetests) and language checking
         */
        stage('Install testing dependency') {
            steps {
                echo 'Initial virtual environment'
                dir("${workspace}") {
                    sh "python3 -m venv .venv"
                }

                echo 'Install testing dependency'
                /**
                 * withPythonEnv 函数需要 Jenkins Pyenv plugin 支持
                 */
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        sh 'apk add --no-cache py3-qt5 libffi-dev openssl-dev'
                        sh 'sed "s/^PyQt5/#PyQt5/" -i requirements.txt'
                        sh 'pip install wheel nose coverage nosexcover pylint twine'
                        sh 'pip install -r requirements.txt'
                        sh 'pip list'
                    }
                }
            }
        }

        /**ocker
         * Run coverage or regular unit test
         */
        stage('Testing') {
            steps {
                echo 'Run test cases'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        // sh 'python setup.py test'
                        sh 'nosetests -sv --with-xunit --xunit-file=nosetests.xml --with-xcoverage --xcoverage-file=coverage.xml'
                    }
                }
            }
        }

        /**
         * Call SonarQube scanner
         * It will load in coverage and other reports generated from previous step.
         */
        stage('Sonar scan') {
            steps {
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        script {sonarHome=tool 'SonarQube Scanner'}    // name is defined in `Global Tool Configuration`
                        withSonarQubeEnv('MySonarQube') {                      // name is defined in `Configure System`
                            sh 'echo workspace=${sonarHome}'
                            sh 'sonar-scanner \
                                -Dsonar.host.url=http://192.168.10.65:9000 \
                                -Dsonar.projectKey=Dashboard \
                                -Dsonar.projectVersion=1.0 \
                                -Dsonar.language=py \
                                -Dsonar.tests=./tests \
                                -Dsonar.exclusions=setup.py,**/__init__.py \
                                -Dsonar.sourceEncoding=UTF-8 \
                                -Dsonar.python.xunit.reportPath=nosetests.xml \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.python.pylint=/usr/local/bin/pylint \
                                -Dsonar.python.pylint_config=.pylintrc \
                                -Dsonar.python.pylint.reportPath=pylint-report.txt'
                        }
                    }
                }
        
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        /**
         * Package
         *
         * 关于 Python 版本规范：https://www.python.org/dev/peps/pep-0440/
         */
        stage('Build') {
            steps {
                echo 'Build Dashboard'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        sh 'sed "s/^#PyQt5/PyQt5/" -i requirements.txt'
                        sh 'python setup.py egg_info -b.dev$(date "+%s") bdist_wheel'
                    }
                }
            }
        }

        /**
         * Pushing to Nexus
         *
         * Run the following commands on client:
         *   pip config set global.index http://192.168.10.65:8081/repository/pypi-central/simple/
         *   pip config set global.index-url http://192.168.10.65:8081/repository/pypi-central/simple/
         *   pip config set global.trusted-host 192.168.10.65
         *   pip config set global.extra-index-url http://192.168.10.65:8081/repository/pypi/simple/
         */
        stage('Pushing to Repository') {
            steps {
                echo 'Upload Dashboard'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        withCredentials([usernamePassword(credentialsId: "${env.PYPI_CREDENTIAL}", passwordVariable: 'pass', usernameVariable: 'user')]){
                            sh '''cat << EOF > .pypirc
[distutils]
    index-servers=
        internal_pypi

[internal_pypi]
    repository: http://192.168.10.65:8081/repository/pypi/
    username: ${user}
    password: ${pass}
EOF'''

                            sh 'twine upload --config-file=.pypirc -r internal_pypi dist/*'
                        }
                    }
                }
            }
        }
    }

    /**
     * 构建后行为
     */
    post{
        // 总是执行
        always{
            echo "Always"
        }

        // 条件执行
        success {
            echo currentBuild.description = "Success"    // currentBuild.description 会将信息带回控制面板
            /**
            emailext (
                subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
            )
            */
        }

        failure{
            echo  currentBuild.description = "Failure"
            /**
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]                                            
            )
            */
        }

        aborted{
            echo currentBuild.description = "Aborted"
            /**
            emailext (
                subject: "Aborted: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>ABORTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]                                            
            )
            */
        }
    }
}
