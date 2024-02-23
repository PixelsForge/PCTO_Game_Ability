"""
Starting a Stream

This example shows how to search for available Muses and
create a new stream
"""

from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop
import utils
import time
import numpy as np

BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0]

# start the communication with the MUSE
stream("00:55:da:b5:49:3e", ppg_enabled=True, acc_enabled=True, gyro_enabled=True)  # "00:55:da:b5:49:3e" = MAC ADDRESS MUSE
streams_EEG = resolve_byprop("type", "EEG", timeout=2)  # it triggers the EEG signals, which are used to find concentration
streams_Gyro = resolve_byprop("type", "Gyroscope", timeout=2)  # starts the gyroscope
# print(streams_EEG)
# second inlet for EEG
inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12)
info_Gyro = inlet_Gyro.info()

inlet_EEG = StreamInlet(streams_EEG[0], max_chunklen=12)
info_EEG = inlet_EEG.info()

fs_Gyro = int(info_Gyro.nominal_srate())  # gyro frequency
fs_EEG = int(info_EEG.nominal_srate())  # frequency EEG signals

listaComandi = [None]

def museDxSx():
    """ACQUIRE LATERAL DIRECTION WITH ACCELEROMETER"""
    # Obtain EEG data from the LSL stream
    gyro_data, timestamp = inlet_Gyro.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
    
    Theta = (0.5 * (gyro_data[-1][2] + gyro_data[-2][2]) * 1 / fs_Gyro)  # speed in this instant, average of the last 2 values, per gyroscope
    print(Theta)
    print(listaComandi)
    comando = None
    if(len(listaComandi) == 1):

        if(Theta > 0.5): #va a sinistra
            comando = 'A'
            ##print("Gyroscope: ", comando)
            listaComandi.append(comando)
        elif(Theta < -0.5): #va a destra
            comando = 'D'
            ##print("Gyroscope: ", comando)
            listaComandi.append(comando)
        else:
            comando = 'W' #rimane dritto
            #print("Gyroscope: ", comando)
            listaComandi.append(comando)
    
    elif(Theta > 0.5 and listaComandi[-2] == 'W'):
        comando = 'A'
        #print("Gyroscope: ", comando)
    elif(Theta < -0.5 and listaComandi[-2] == 'A'):
        comando = 'W'
        #print("Gyroscope: ", comando)
    elif(Theta < -0.5 and listaComandi[-2] == 'W'):
        comando = 'D'
        #print("Gyroscope: ", comando)
    elif(Theta > 0.5 and listaComandi[-2]== 'D'):
        comando = 'W'
        #print("Gyroscope: ", comando)
        
    elif(Theta > 0.5 and listaComandi[-2] == 'A'):
        comando = 'A'
        #print("Gyroscope: ", comando)
    elif(Theta < -0.5 and listaComandi[-2] == 'D'):
        comando = 'D'
        #print("Gyroscope: ", comando)
        
    if len(listaComandi) > 1:
        if comando == None:
            listaComandi.append(listaComandi[-1])
        else:
            listaComandi.append(comando)
            
    return comando  # the command that will enter the alphabot

def museConcentrazione():
    # returns the incoming command to the alphabot for concentration
    eeg_buffer = np.zeros((int(fs_EEG * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter
    EEG_data, timestamp = inlet_EEG.pull_chunk(
        timeout=1, max_samples=int(SHIFT_LENGTH * fs_EEG)
    )
    ch_data = np.array(EEG_data)[:, INDEX_CHANNEL]
    eeg_buffer, filter_state = utils.update_buffer(
        eeg_buffer, ch_data, notch=True, filter_state=filter_state
    )

    """COMPUTE BAND POWERS"""
    data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs_EEG)
    band_powers = utils.compute_band_powers(data_epoch, fs_EEG)  # band_powers(raggi alpha, beta, theta, delta) cioè tutti gli EEG
    #print(band_powers)
    band_beta = utils.compute_beta(data_epoch, fs_EEG)  # compute_beta function for calculating beta rays (concentration)

    """     
    a second method         
    print(EEG_data[-1]) #raggi beta
    Beta = 0.5*(EEG_data[-1][2] + EEG_data[-2][2]) * 1/fs_EEG #speed in this instant
    print(Beta)
    if(Beta > 2):
        print('concentrato')
    else:
        print('non concentrato')
    """
    return band_beta  # command (Avanti / Fermo) for the alphabot, if concentrated Avanti then go ahead, otherwise Fermo, stand still

def main():

    while True:
        Direzione = museDxSx()
        Movimento = museConcentrazione()
        #print("concentrazione: ", Movimento)
        #print("Movimento: ", Direzione)
        #time.sleep(0.3)
        print("----------------------------------------------------------------")


if __name__ == "__main__":
    main()