#https://www.youtube.com/watch?v=xTiaIuHM52A&ab_channel=Geek
import pymem
import time
import dearpygui.dearpygui as gui
import threading
pm = pymem.Pymem("Csgo.exe")
base = pymem.pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll


#offsets
dwLocalPlayer = 0xDEA964
m_iHealth = 0x100
m_iCrosshairId = 0x11838
m_iTeamNum = 0xF4
dwEntityList = 0x4DFFFC4
dwForceAttack = 0x322DDFC
m_vecVelocity = 0x114




def Triggerbot():
    while True:
        if gui.get_value('TriggerBotState'):
            LocalPlayer = pm.read_uint(base + dwLocalPlayer)
            if not LocalPlayer: continue
            if pm.read_uint(LocalPlayer + m_iHealth) <= 0: continue

            crosshair = pm.read_uint(LocalPlayer + m_iCrosshairId)
            LocalTeam = pm.read_uint(LocalPlayer + m_iTeamNum)
            EntityTeam = pm.read_uint(base + dwEntityList + (crosshair - 1) * 0x10)
            crosshairTeam = pm.read_uint(EntityTeam + m_iTeamNum)

            if LocalTeam == crosshairTeam: continue

            if crosshair >= 1 and crosshair <= 20:
                time.sleep(gui.get_value('TriggerBotDelayBefore'))
                pm.write_uint(base + dwForceAttack, 6)
                time.sleep(gui.get_value('TriggerBotDelayAfter'))



def Bhop():
    while True:
        LocalPlayer = pm.read_uint(base + dwLocalPlayer)
        if not LocalPlayer: continue
        if pm.read_uint(LocalPlayer + m_iHealth) <= 0: continue

        Velocity = pm.read_uint(LocalPlayer +  m_vecVelocity)

        if not Velocity == 0:
            print(Velocity)
            pm.write_uint(LocalPlayer + int(gui.get_value('VelocitySlider')), 4)

gui.create_context()
gui.create_viewport(title='Only use for experimental purposes', width=500, height=450)
gui.setup_dearpygui()
gui.set_viewport_always_top(True)

with gui.window(label='CSGO Cheat', width=500, height=450, no_title_bar=True, no_resize=True, no_move=True):
    with gui.tab_bar(label="Tabs"):

        with gui.tab(label='Aiming'):
            gui.add_checkbox(label='Triggerbot', tag='TriggerBotState')
            gui.add_slider_float(label='Delay before shooting', tag='TriggerBotDelayBefore', min_value=0, max_value=1)
            gui.add_slider_float(label='Delay after shooting', tag='TriggerBotDelayAfter', min_value=0, max_value=1)

        with gui.tab(label='Movement'):
            gui.add_checkbox(label='BHop', tag='BHOPState')
            gui.add_checkbox(label='Velocity Changer', tag='Velocity')
            gui.add_slider_float(label='Velocity', tag='VelocitySlider', min_value=0, max_value=2)

threading.Thread(target=Triggerbot).start()
threading.Thread(target=Bhop).start()

gui.show_viewport()
gui.start_dearpygui()
gui.destroy_context()
