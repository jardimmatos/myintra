<template>
    <span>
        <v-row>
            <!-- AREA DE CAMERA ou ARQUIVO -->
            <v-col sm="12" md="4" lg="4">
                <div class="col-video-file">
                    <video ref="video" class="border-radius-7" autoplay></video>
                    <v-btn class="mb-1 btn-take" title="Tirar Foto" icon :tile="false"
                        @click="takePhoto" :loading="loading" v-show="cameraIsOn">
                        <v-icon small>mdi-camera</v-icon>
                    </v-btn>
                    <span v-if="cameraIsOn">
                        <!-- EXIBIR BOTÃO de DESLIGAR CAMERA SE CAMERA ESTIVER LIGADA -->
                        <v-btn class="mb-1 btn-off" title="Desligar" icon :tile="false"
                            @click="turnoffCamera" :disabled="loading">
                            <v-icon color="error">mdi-power</v-icon>
                        </v-btn>
                    </span>
                    <span v-else>
                        <!-- EXIBIR BOTÃO de LIGAR CAMERA SE CAMERA ESTIVER DESLIGADA -->
                        <v-btn class="mb-1 btn-on" title="Ligar Câmera" icon :tile="false"
                            @click="turnonCamera" :loading="loading">
                            <v-icon color="success">mdi-power</v-icon>
                        </v-btn>
                    </span>
                </div>
                <!-- OPCÃO para carregamento de arquivo -->
                <v-file-input  hide-details
                    v-model="file_field"
                    class="mt-4"
                    prepend-icon="mdi-upload"
                    @update:modelValue="onFileChange"
                    ref="inputFile" label="Carregar uma imagem"
                    placeholder="Carregar de arquivo" accept=".jpg, .png, .bmp"></v-file-input>
            </v-col>
            <!-- AREA DE CROP -->
            <v-col sm="12" md="4" lg="4">
                <div v-show="!!this.imageDataUrl">
                    <canvas ref="canvas" :width="1327" :height="1000" style="display: none;" class="border-radius-7"></canvas>
                    <div ref="imageContainer" class="preview_crop border-radius-7" style="width:100% !important;"></div>
                </div>
            </v-col>
            <!-- RESULTADO DO CROP -->
            <v-col sm="12" md="4" lg="4" class="px-4">
                <!-- PREVIEW DE IMAGEM SELECIONADA -->
                <div v-show="imageDataUrlCropped" style="text-align: -webkit-center;">
                    <v-img :src="imageDataUrlCropped" class="selected-image border-radius-7 mb-2"></v-img>
                    <v-row class="px-2">
                        <v-btn color="info" small class="mb-1 btn-clean" :disabled="loading"
                                @click="cleanPhoto">Limpar</v-btn>
                        <v-spacer></v-spacer>
                        <!-- CONSIDERAR VERDE APENAS STATUS 1(OK) ou 99 (SEM NADA) -->
                        <v-btn :color="[1,99].includes(imageTestedCode) ? 'success' : 'error'"
                                small class="mb-1" :disabled="loading"
                                @click="selectPhoto" v-show="imageTestedCode || true">Validar foto</v-btn>
                    </v-row>
                    <v-row justify="center" class="my-4">
                        <h3 :class="imageTestedCode == 1 ? 'text-success' : 'text-error'">
                            {{resultTest[imageTestedCode]}}
                        </h3>
                    </v-row>
                    <v-row justify="center" class="my-4" v-show="imageTestedCode == 1" >
                        <v-btn @click="selectCropped" small color="success">Selecionar Imagem</v-btn>
                    </v-row>
                </div>
            </v-col>
        </v-row>
    </span>
</template>
<script>
import Cropper from 'cropperjs';
import { mapGetters } from 'vuex';
import 'cropperjs/dist/cropper.min.css';
import { mapActions } from 'vuex';
export default {
    props:{
        power:{ // criada para dinamizar o true/false de um dialog
            default: false,
        }
    },
    data:()=>({
        loading:false,
        stream:null,
        cropper: null,
        imageDataUrl: null,
        imageDataUrlCropped: null,
        cameraIsOn:false,
        resultTest:{
            0  : 'Status desconhecido',
            1  : 'Foto liberada para cadastro',
            2  : 'Rosto muito longe',
            3  : 'Rosto muito perto',
            4  : 'Face não centralizada',
            5  : 'Postura do rosto não centralizada',
            6  : 'Baixa Nitidez',
            7  : 'Rosto não detectado',
            8  : 'Face já existente',
            9  : 'Tamanho de imagem desconhecido',
            10 : 'Imagem Pequena',
            11 : 'Imagem muito grande',
            12 : 'Usuário não existe',
            13 : 'Muitas faces já estão cadastradas no dispositivo',
            14 : 'Rosto muito perto das bordas da imagem',
            99 : '', // fictício
        },
        imageTestedCode: 99,
        file_field:null //v-model apenas para limpar campo de arquivo após selecionar o cropp
    }),
    mounted(){
        this.turnonCamera()
    },
    methods: {
        ...mapActions(['TestImage']),
        selectCropped(){
            /* Não usando, está sendo capturado pelo $ref */
            const croppedurl = this.imageDataUrlCropped
            this.$emit('on-selected-image', croppedurl)
            this.file_field = null
        },
        turnonCamera(){
            this.openCamera()
        },
        openCamera(){
            this.turnoffCamera()
            this.loading = true
            // Abre a câmera do dispositivo e captura a foto
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    this.stream = stream
                    this.$refs.video.srcObject = stream;
                    this.cameraIsOn = true
                })
                .catch(error => {
                    console.error('Erro ao abrir a câmera:', error);
                    this.cameraIsOn = false
                }).finally(()=>{
                    this.loading = false
                });
        },
        onFileChange(event) {
            if (!event){
                return
            }
            /* Método utilizado ao selecionar de um arquivo */
            /* limpar */
            this.cleanPhoto()
            // const file = event.target.files[0]; # usando com input padrao html
            const file = event[0]; // usando com v-file-input
            const reader = new FileReader();
            reader.onload = (e) => {
                this.createCropper(e.target.result);
                this.imageDataUrl = e.target.result
            };
            reader.readAsDataURL(file);
        },
        takePhoto() {
            const video = this.$refs.video;
            const canvas = this.$refs.canvas;
            const context = canvas.getContext('2d');

            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            this.imageDataUrl = canvas.toDataURL('image/jpeg');
            
            this.createCropper(this.imageDataUrl);
        },
        createCropper(imageUrl) {
            this.destroyCropper(); // Destroi o cropper anterior, se existir
            const imageContainer = this.$refs.imageContainer;
            const image = new Image(400,400);
            image.onload = () => {
                this.cropper = new Cropper(image, {
                    aspectRatio: 1, // Define a proporção de recorte (1:1 para uma imagem quadrada)
                    viewMode: 2, // Habilita o modo de visualização de recorte
                    autoCropArea: 0.65, // Define a proporção da área de recorte em relação à imagem
                    guides:true, // guias de gride
                    rotatable:true,
                    responsive:true,
                    crop: (event) => {
                        event
                        this.cropImage()
                        // Função de callback chamada quando a imagem é recortada
                        // console.log('Nova área de recorte:', event.detail);
                    }
                });
            };
            image.src = imageUrl;
            imageContainer.appendChild(image);
        },
        cropImage() {
            // Captura a imagem recortada em base64
            const croppedImageDataUrl = this.cropper.getCroppedCanvas().toDataURL('image/jpeg');
            this.imageDataUrlCropped = croppedImageDataUrl;
        },
        destroyCropper() {
            // Destroi o cropper atual, se existir
            if (this.cropper) {
                this.cropper.destroy();
                this.cropper = null;
                this.$refs.imageContainer.innerHTML = '';
            }
        },
        cleanPhoto(){
            this.imageDataUrl = null
            this.imageDataUrlCropped = null
            this.imageTestedCode = 99
        },
        turnoffCamera(){
            this.cleanPhoto()
            if (this.stream) {
                this.stream.getTracks().forEach((track) => {
                    track.stop();
                });
            }
            this.cameraIsOn = false
        },
        async testImage(){
            this.loading = true
            let img_cropped = this.imageDataUrlCropped
            img_cropped = img_cropped.split(';base64,')
            let response = await this.TestImage({image: img_cropped[1]})
            if (response.status == 200){
                /*
                    A resposta é um número, se -1, o dispositivo onde está ocorrendo o
                    test não tem dispositivo de câmera, se a resposta for de 0 a 14,
                    cada um representa um status na variável data this.resultTest
                */
                this.imageTestedCode = response.data
            }
            this.loading = false
        },
        async selectPhoto(){
            this.testImage()
        },
    },
    computed:{
        ...mapGetters(['StateDark']),
    },
    watch:{
        imageDataUrlCropped: {
            handler(){
                this.imageTestedCode = 99
            }
        },
        power(value){
            if(value){
                this.turnonCamera()
            }else{
                this.turnoffCamera()
            }
        }
    },
    beforeUnmount() {
        // Para o vídeo e libera a câmera quando o componente for destruído
        this.turnoffCamera()
    },
};
</script>
<style scoped>
video{
    width: 100%;
    /* border-radius: 7px; */
    max-height: 50%;
    /* max-width: 340px; */
}
.border-radius-7, .cropper-container{
    border-radius: 7px !important;
}
.selected-image{
    /* border: 5px solid green ; */
    max-height: 340px;
    max-width: 340px;
}
.col-video-file{
    /* parent relative */
    position: relative;
}
.btn-on, .btn-off{
    /* son 1 absolute */
    position: absolute;
    left: 15px;
    bottom: 10px;
}
.btn-take{
    /* son 2 absolute */
    position: absolute;
    right: 10px;
    bottom: 10px;
}
.cropper-bg{
    height: 370px !important;
}
</style>