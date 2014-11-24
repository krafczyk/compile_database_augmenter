project(compile_database_augmenter)

cmake_minimum_required(VERSION 2.8)

#Setup python variables
execute_process(COMMAND which python
                RESULT_VARIABLE Python_result
                OUTPUT_VARIABLE PYTHON)

if(NOT(Python_result EQUAL 0))
message(FATAL "Failed to find python!")
endif()

string(STRIP ${PYTHON} PYTHON)

message(STATUS "Found python executable: (${PYTHON})")

execute_process(COMMAND "${PYTHON}" "--version"
                RESULT_VARIABLE Python_version_result
                OUTPUT_VARIABLE Python_version_stdout
                ERROR_VARIABLE Python_version_output)

if(NOT(Python_version_result EQUAL 0))
message(FATAL_ERROR "Failed to get python version! (${Python_version_result})")
endif()

string(STRIP ${Python_version_output} Python_version_output)

execute_process(COMMAND echo "${Python_version_output}"
                COMMAND awk "{print $2}"
                RESULT_VARIABLE Python_version_result
                OUTPUT_VARIABLE PYTHON_VERSION)

if(NOT(Python_version_result EQUAL 0))
message(FATAL_ERROR "Failed to parse python version!")
endif()

string(STRIP ${PYTHON_VERSION} PYTHON_VERSION)

message(STATUS "Python is version (${PYTHON_VERSION})")

configure_file(
	"${CMAKE_CURRENT_SOURCE_DIR}/py/compile_database_augmenter.in"
	"${CMAKE_CURRENT_BINARY_DIR}/compile_database_augmenter"
	IMMEDIATE @ONLY)

install(FILES py/compile_database_augmenter.py ${CMAKE_CURRENT_BINARY_DIR}/compile_database_augmenter DESTINATION bin PERMISSIONS OWNER_READ OWNER_EXECUTE GROUP_READ GROUP_EXECUTE)
