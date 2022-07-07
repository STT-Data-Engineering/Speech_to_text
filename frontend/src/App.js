import './App.css';
import AudioReactRecorder, { RecordState } from 'audio-react-recorder';
import {useState} from "react";
import 'audio-react-recorder/dist/index.css'
import {MicrophoneIcon} from "@heroicons/react/solid";
import { Icon } from '@iconify/react';
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'
import axios from 'axios';

function App() {
    const [recordState, setRecordState] = useState(null);
    const [audioData, setAudioData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [sentence, setSentence] = useState('hey');
    const Spinner = require('react-spinkit');

    const stop = () => {
        setRecordState(RecordState.STOP)
    }

    const start = () => {
        setRecordState(RecordState.START)
    }

    const pause = () => {
        setRecordState(RecordState.PAUSE)
    }

    const clear = () => {
        setRecordState(null);
        setAudioData(null);
    }

    const loadText = () => {
        axios({
            method: 'GET',
            url: 'http://localhost:8888/get_text',
        })
        .then((response) => {
            setSentence(response.data.text)
        })
        .catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
                }
        })
        
        
    }

    const upload = () => {
        setLoading(true);
        console.log('uploading...')
        // const data = new FormData();
        // data.append("file", audioData["blob"]);
        // let url = "http://localhost:8888/submit";

        // axios.post(url, data).then((res) => {
        //     const { data } = res;

            

        //     setLoading(false);
        // });
        const data = new FormData();
        data.append("file", audioData["blob"]);
        console.log(data)
        axios({
            method: 'POST',
            url: 'http://localhost:8888/submit',
            data: {
                    
                    sentence: sentence,
                    transcription: data
                }

        })
        .then((response) => {
            console.log("sent transcription")
            
        })
        .catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
                }
            })
        setLoading(false);
    }

    const skip = () => {
        setLoading(true);
        loadText();
        
        clear();
        setLoading(false);
        
    }

    const onStop = (data) => {
        setAudioData(data);
    }

    return (
      <div className="flex flex-col w-full h-screen items-center">
          <div className="grow" style={{textAlign: '-webkit-center'}}>
              <div className={` ${recordState === RecordState.STOP ? 'visible' : 'invisible'} flex flex-row space-x-4 justify-center mt-6`}>
                  <button onClick={upload} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                      <span className='text-white text-2xl'>ላክ</span>
                      <Icon className='ml-6 self-center' icon="bi:cloud-upload-fill" color="white"  width="24" height="24" />
                  </button>
                  <button onClick={clear} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                      <span className='text-white text-2xl'>አጸዳ</span>
                      <Icon className='ml-6 self-center' icon="fluent:delete-16-filled" color="white"  width="24" height="24" />
                  </button>
              </div>
              <div className="">
                  <AudioReactRecorder state={recordState} onStop={onStop} backgroundColor='rgb(255,255,255)'/>
                  <audio id='audio' controls src={audioData ? audioData.url : null} />
              </div>
              <MicrophoneIcon className="h-64 w-64 mb-12 text-[#0069A5] text-center"/>
              {recordState === RecordState.START || recordState === RecordState.PAUSE ?
                  <div className='flex flex-row space-x-4 justify-center'>
                      <button onClick={stop} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                          <span className='text-white text-2xl'>አቁም</span>
                          <Icon className='ml-6 self-center' icon="bi:stop-circle-fill" color="white"  width="24" height="24" />
                      </button>
                      {recordState === RecordState.PAUSE ?
                          <button onClick={start} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                              <span className='text-white text-2xl'>ቀጥል</span>
                              <Icon className='ml-6 self-center' icon="bi:play-circle-fill" color="white"  width="24" height="24" />
                          </button>
                          :
                          <button onClick={pause} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                              <span className='text-white text-2xl'>ለአፍታ አቁም</span>
                              <Icon className='ml-6 self-center' icon="bi:pause-circle-fill" color="white"  width="24" height="24" />
                          </button>
                      }

                  </div>
                  :
                  loading ? <Spinner name="line-scale-pulse-out" color='#0069A5' className='w-24 h-24'/> :
                  <button onClick={start} className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded inline-flex">
                      <span className='text-white text-2xl'>ቅዳ</span>
                      <Icon className='ml-6 self-center' icon="entypo:controller-record" color="#d40000"  width="24" height="24" />
                  </button>
              }
          </div>
          <div className='flex flex-row m-12 space-x-32'>
              {loading ?
                  <Skeleton height={30} width={1000} count={2} />
                  :
                  <p className='text-2xl text-center font-bold'>
                      {
                      sentence
                      }

                  </p>
              }


              {!loading &&
                  <div className='pr-20'>
                      <button onClick={skip}
                              className="bg-[#0069A5] hover:bg-grey text-grey-darkest font-bold py-2 px-4 rounded-full inline-flex items-center">
                          <div className='flex flex-row'>
                              <span className='text-white text-2xl'>ዝለል</span>
                              <Icon className='ml-6 self-center' icon="fluent:skip-forward-tab-20-filled" color="white"
                                    width="24" height="24"/>
                          </div>
                      </button>
                  </div>
              }
            </div>
      </div>
    );
}

export default App;
