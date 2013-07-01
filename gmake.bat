@echo off

bin\premake4 gmake
make -j4
IF %ERRORLEVEL% neq 0 GOTO ERROR_END

pushd bullet
..\bin\premake4 gmake
make -j4
IF %ERRORLEVEL% neq 0 GOTO ERROR_END
popd

pushd irrlicht
..\bin\premake4 gmake
make -j4
IF %ERRORLEVEL% neq 0 GOTO ERROR_END
popd

pushd irrlicht\irrext
..\..\bin\premake4 gmake
make -j4
IF %ERRORLEVEL% neq 0 GOTO ERROR_END
popd

pushd irrlicht\examples
..\..\bin\premake4 gmake
make -j4
IF %ERRORLEVEL% neq 0 GOTO ERROR_END
popd

echo !! success !!
exit

:ERROR_END
echo !! error occured !!

