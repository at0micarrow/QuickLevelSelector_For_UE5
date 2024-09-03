import unreal

processed_menu_entry_cache = []
entry_counter = 0

@unreal.uclass()
class ComboButtonMenu(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        unreal.log("exec")

@unreal.uclass()
class LevelEntry(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        open_level(self.data.name)

@unreal.uclass()
class RefreshButton(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        check_levels()

#Added this class to store the cache the data. I have to find out how to store data in the uclass.
class LevelEntryWrapper:
    def __init__(self, menu_entry=unreal.ToolMenuEntryScript):
        self.menu_entry= menu_entry

    def get_menu_entry(self):
        return self.menu_entry

    def get_package_name(self):
        return self.menu_entry.data.name

################################################################################

def run():
    # Use a custom owner name for the menu entry.
    menu_owner = "LevelEditor_ToolbarExtension_OpenLevel"
    # Retrieve the tool menus manager.
    tool_menus = unreal.ToolMenus.get()
    # Locate the target menu (a ToolMenu object) where the combo button will be added.
    target_menu = tool_menus.find_menu("LevelEditor.LevelEditorToolBar.ModesToolBar")
    # Extend the target menu with a new submenu identified by the "OpenLevel" name.
    tool_menus.extend_menu(f"{target_menu.menu_name}.OpenLevel")
    # Create an instance of our custom ToolMenuEntryScript class (ComboButtonMenu).
    toolbar_combo_menu = ComboButtonMenu()
    # Define the data for the combo button menu entry.
    toolbar_combo_menu_data = unreal.ToolMenuEntryScriptData(
        menu=target_menu.menu_name,
        section="File",
        name="OpenLevel",
        label="Open Level",
        tool_tip="Displays the available levels in the project",
        icon=unreal.ScriptSlateIcon("EditorStyle", "LevelEditor.OpenLevel"),
        owner_name=menu_owner,
        advanced=unreal.ToolMenuEntryScriptDataAdvanced(
            entry_type=unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON,
            user_interface_action_type=unreal.UserInterfaceActionType.CHECK
        )
    )
    # Assign the menu data to the combo button instance.
    toolbar_combo_menu.data.assign(toolbar_combo_menu_data)
    # Add the combo button to the target menu and register it.
    target_menu.add_menu_entry_object(toolbar_combo_menu)

    #TODO: I want to change this to an auto refresh solution in the future but I didn't find any add_callable option in the asset registry to do so. If I have time I'll add the delegate in the source to the asset registry if any asset is deleted or created it will call this delegate.

    #Create Refresh Button
    refresh_entry = RefreshButton()
    refresh_entry.init_entry(owner_name="LevelEditor_ToolbarExtension_Refresh_Button", 
                            menu="LevelEditor.LevelEditorToolBar.ModesToolBar.OpenLevel",
                            section="",
                            name="RefreshButton",
                            label="Refresh",
                            tool_tip="Refresh the Level list")
    refresh_entry.data.icon = unreal.ScriptSlateIcon("EditorStyle", "SourceControl.Actions.Refresh")
    refresh_entry.data.advanced.entry_type.MENU_ENTRY

    tool_menus.add_menu_entry_object(refresh_entry)

    #Sort the levels and create the entries for it.
    populate_level_entries(menu_owner="LevelEditor_ToolbarExtension_OpenLevel_Entries",
                        target_menu="LevelEditor.LevelEditorToolBar.ModesToolBar.OpenLevel")


# Populate the combo box with levels
def populate_level_entries(menu_owner: unreal.Name = "None", target_menu: unreal.Name = "None"):

    tool_menus = unreal.ToolMenus.get().find_menu(target_menu)
    unreal.ToolMenus.get().unregister_owner_by_name(menu_owner)
    unreal.ToolMenus.get().refresh_menu_widget(target_menu)

    # Fetch all levels
    levels = get_all_levels()
    entry_counter = 0

    # Group levels by section name
    grouped_levels = {}
    for level in levels:
        section_name = level[1]
        if section_name not in grouped_levels:
            grouped_levels[section_name] = []
        grouped_levels[section_name].append(level)

    # Sort sections: "Game" first, "Engine" last, others in between
    sorted_sections = sorted(grouped_levels.keys(), key=lambda s: (s != "Game", s == "Engine", s))

    # Add sections and levels to the menu
    for section_name in sorted_sections:
        tool_menus.add_section(section_name, section_name)

        # Sort levels alphabetically by asset_name within each section
        sorted_levels = sorted(grouped_levels[section_name], key=lambda level: level[0])

        for level in sorted_levels:
            asset_name = level[0]
            package_path = level[2]
            package_name = level[3]

            # Check if the package name is already processed
            cached_entry_found = False
            for cached_menu_entry in processed_menu_entry_cache:
                if isinstance(cached_menu_entry, LevelEntryWrapper):
                    if cached_menu_entry.get_package_name() == package_name:
                        tool_menus.add_menu_entry_object(cached_menu_entry.get_menu_entry())
                        #unreal.log("Used cached level entry")
                        entry_counter += 1
                        cached_entry_found = True
                        break  # No need to continue checking other cached entries

            if not cached_entry_found:
                menu_entry = LevelEntry()
                menu_entry.init_entry(menu_owner, target_menu, section_name, package_name, asset_name, package_path)
                menu_entry.data.advanced.entry_type.MENU_ENTRY
                
                level_entry_wrapper = LevelEntryWrapper(menu_entry)
                tool_menus.add_menu_entry_object(menu_entry)
                processed_menu_entry_cache.append(level_entry_wrapper)
                #unreal.log("Created new entry")
                entry_counter += 1

# Get all levels in the project
def get_all_levels():
    asset_registry_helper = unreal.AssetRegistryHelpers.get_asset_registry()
    
    # The class path name should be provided as a TopLevelAssetPath
    world_class_path = unreal.TopLevelAssetPath("/Script/Engine.World")

    # List to store the tuples
    asset_data = []

    levels = asset_registry_helper.get_assets_by_class(world_class_path, True)
    for level in levels:
        
        if isinstance(level, unreal.AssetData):
            asset_name = level.asset_name
            package_path = level.package_path
            package_name = level.package_name
            # Extract the first part of the package path as the section name
            section_name = str(package_path).split('/')[1]
            # Store the variables as a tuple and add it to the list
            asset_data.append((asset_name, section_name, package_path, package_name))
    return asset_data

# Open the selected level
def open_level(level_path):
    subsystem = unreal.LevelEditorSubsystem()
    subsystem.save_current_level()
    subsystem.load_level(level_path)

def check_levels():
    levels =unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine.World"), True)
    if len(levels) != entry_counter:
        populate_level_entries(menu_owner="LevelEditor_ToolbarExtension_OpenLevel_Entries",
                        target_menu="LevelEditor.LevelEditorToolBar.ModesToolBar.OpenLevel")
    
"""   
import threading

def timer_action():
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        unreal.log(f"Action performed at: {current_time}")
        #unreal.SystemLibrary().ti
        #unreal.SystemLibrary().execute_console_command(None,'RunPython "run_again()"')
        time.sleep(2)

# Create and start the timer thread
timer_thread = threading.Thread(target=timer_action, daemon=True)
timer_thread.start()

# The main thread can continue running other tasks
# For example, if you're running this within Unreal, the editor remains responsive
"""