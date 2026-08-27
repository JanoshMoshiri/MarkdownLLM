Unicode True
RequestExecutionLevel user
SetCompressor /SOLID lzma

!include "MUI2.nsh"
!include "nsDialogs.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"

!ifndef APP_VERSION
  !error "APP_VERSION is required"
!endif
!ifndef FROZEN_DIR
  !error "FROZEN_DIR is required"
!endif
!ifndef OUTPUT_DIR
  !error "OUTPUT_DIR is required"
!endif
!ifndef APP_ICON
  !error "APP_ICON is required"
!endif

!define APP_NAME "MarkdownLLM Explorer"
!define APP_REGISTRY "Software\MarkdownLLM Explorer"
!define UNINSTALL_REGISTRY "Software\Microsoft\Windows\CurrentVersion\Uninstall\MarkdownLLM Explorer"

Name "${APP_NAME}"
Caption "${APP_NAME} Setup"
OutFile "${OUTPUT_DIR}\MarkdownLLM-Explorer-Installer-${APP_VERSION}.exe"
InstallDir "$LOCALAPPDATA\Programs\MarkdownLLM Explorer"
InstallDirRegKey HKCU "${APP_REGISTRY}" "InstallDir"
Icon "${APP_ICON}"
UninstallIcon "${APP_ICON}"
BrandingText "MarkdownLLM"
ShowInstDetails nevershow
ShowUninstDetails nevershow

Var SubstrateRoot
Var RootInput

!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Open MarkdownLLM Explorer"
!define MUI_FINISHPAGE_RUN_FUNCTION LaunchExplorer

!insertmacro MUI_PAGE_WELCOME
Page custom RootPageCreate RootPageLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Function .onInit
  SetShellVarContext current
  ${GetParameters} $0
  ClearErrors
  ${GetOptions} $0 "/SUBSTRATEROOT=" $SubstrateRoot
  ${If} ${Errors}
    ReadRegStr $SubstrateRoot HKCU "${APP_REGISTRY}" "SubstrateRoot"
  ${EndIf}

  ${If} $SubstrateRoot == ""
    ${GetParent} "$EXEDIR" $0
    ${GetParent} "$0" $1
    ${If} ${FileExists} "$1\AGENTS.md"
      StrCpy $SubstrateRoot "$1"
    ${EndIf}
  ${EndIf}

  ${If} ${Silent}
    ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
      SetErrorLevel 2
      Quit
    ${EndIf}
  ${EndIf}
FunctionEnd

Function un.onInit
  SetShellVarContext current
FunctionEnd

Function RootPageCreate
  nsDialogs::Create 1018
  Pop $0
  ${If} $0 == error
    Abort
  ${EndIf}

  ${NSD_CreateLabel} 0 0 100% 28u "Choose the MarkdownLLM substrate to explore. This is the folder containing its top-level AGENTS.md file."
  Pop $0
  ${NSD_CreateDirRequest} 0 38u 78% 12u "$SubstrateRoot"
  Pop $RootInput
  ${NSD_CreateBrowseButton} 80% 37u 20% 14u "Browse..."
  Pop $0
  ${NSD_OnClick} $0 RootBrowse
  nsDialogs::Show
FunctionEnd

Function RootBrowse
  nsDialogs::SelectFolderDialog "Choose the MarkdownLLM substrate" "$SubstrateRoot"
  Pop $0
  ${If} $0 != error
    ${NSD_SetText} $RootInput "$0"
  ${EndIf}
FunctionEnd

Function RootPageLeave
  ${NSD_GetText} $RootInput $SubstrateRoot
  ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
    MessageBox MB_ICONEXCLAMATION|MB_OK "That folder is not a MarkdownLLM substrate. Choose the folder containing AGENTS.md."
    Abort
  ${EndIf}
FunctionEnd

Function LaunchExplorer
  ExecShell "open" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"'
FunctionEnd

Section "Install" SEC_INSTALL
  ${IfNot} ${FileExists} "$SubstrateRoot\AGENTS.md"
    SetErrorLevel 2
    Abort
  ${EndIf}

  IfFileExists "$INSTDIR\MarkdownLLM Explorer.exe" 0 +2
    ExecWait '"$INSTDIR\MarkdownLLM Explorer.exe" --request-exit --root "$SubstrateRoot"'

  RMDir /r "$INSTDIR\_internal"
  Delete "$INSTDIR\MarkdownLLM Explorer.exe"
  SetOutPath "$INSTDIR"
  File /r "${FROZEN_DIR}\*.*"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "${APP_REGISTRY}" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${APP_REGISTRY}" "SubstrateRoot" "$SubstrateRoot"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "Publisher" "MarkdownLLM"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "DisplayIcon" "$INSTDIR\MarkdownLLM Explorer.exe"
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "${UNINSTALL_REGISTRY}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegDWORD HKCU "${UNINSTALL_REGISTRY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTALL_REGISTRY}" "NoRepair" 1

  CreateDirectory "$SMPROGRAMS\MarkdownLLM Explorer"
  CreateShortcut "$DESKTOP\MarkdownLLM Explorer.lnk" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"' "$INSTDIR\MarkdownLLM Explorer.exe" 0 SW_SHOWNORMAL "" "Explore this MarkdownLLM substrate"
  CreateShortcut "$SMPROGRAMS\MarkdownLLM Explorer\MarkdownLLM Explorer.lnk" "$INSTDIR\MarkdownLLM Explorer.exe" '--root "$SubstrateRoot"' "$INSTDIR\MarkdownLLM Explorer.exe" 0 SW_SHOWNORMAL "" "Explore this MarkdownLLM substrate"
  CreateShortcut "$SMPROGRAMS\MarkdownLLM Explorer\Uninstall MarkdownLLM Explorer.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  IfFileExists "$INSTDIR\MarkdownLLM Explorer.exe" 0 +2
    ExecWait '"$INSTDIR\MarkdownLLM Explorer.exe" --request-exit --root "$INSTDIR"'

  Delete "$DESKTOP\MarkdownLLM Explorer.lnk"
  RMDir /r "$SMPROGRAMS\MarkdownLLM Explorer"
  DeleteRegKey HKCU "${UNINSTALL_REGISTRY}"
  DeleteRegKey HKCU "${APP_REGISTRY}"
  RMDir /r "$INSTDIR"
SectionEnd
