import { Component } from '@angular/core';
import { NgForm, FormControl, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { RGBRangeValidator } from './RGBRangeValidator';
import { MatRadioChange } from '@angular/material/radio';
import { ExcelService } from './excel.service';

export interface Tile {
  color: string;
  text: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  excelFileGroup = new FormGroup({
    excelFileValid: new FormControl(null, Validators.required),
    excelRenderMode: new FormControl(null, Validators.required)
  })

  excelFile: File;

  clickedAddColor: boolean = false;
  addNewColor: boolean = false;
  validColorRed = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorGreen = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorBlue = new FormControl('', [Validators.required, RGBRangeValidator()]);

  tiles: Tile[] = [
    // {text: '1', color: 'lightblue'},
    // {text: '2', color: 'lightgreen'},
    // {text: '3', color: 'lightpink'},
    // {text: '4', color: '#DDBDF1'},
  ];
  defaultTiles = Object.assign([], this.tiles);

  constructor(
    private excelService: ExcelService
  ) {

  }

  addColor() {
    if(this.validColorRed.valid && this.validColorGreen.valid && this.validColorBlue.valid) {
      let color = this.rgbToHex(this.validColorRed.value, this.validColorGreen.value, this.validColorBlue.value);
      let newTile : Tile = {color: color, text: (this.tiles.length + 1).toString()};
      this.tiles.push(newTile);
    }
    this.clickedAddColor = true;
  }

  addColorDialog() {
    this.addNewColor = true;
  }

  onNoClick() {
    this.addNewColor = false;
  }

  resetDefault() {
    this.tiles = Object.assign([], this.defaultTiles);;
  }

  processFile(fileList : FileList) {
    if(fileList[0]) {
      this.excelFile = fileList[0];
    }
    else {
      alert("File was not successfully added. Please try again");
    }
  }

  onSubmit(form) {
    if(form.value.excelRenderMode == "program") {
      this.programValidation(this.excelFile);
    }
    else if(form.value.excelRenderMode == "resource") {
      this.resourceValidation(this.excelFile);
    }
  }

  programValidation(excelFile) {
    this.excelService.sendProgramValidation(excelFile).subscribe( (res: File) => {
      console.log(res);
    },
    err => {
      console.log(err);
    });
  }

  resourceValidation(excelFile) {
    this.excelService.sendResourceValidation(excelFile).subscribe( (res: File) => {
      console.log(res);
    },
    err => {
      console.log(err);
    });
  }

  rgbToHex(r,g,b) { 
    let red = Number(r).toString(16);
    let green = Number(g).toString(16);
    let blue = Number(b).toString(16);
    if (red.length < 2) {
      red = "0" + red;
    }
    if (green.length < 2) {
      green = "0" + green;
    }
    if (blue.length < 2) {
      blue = "0" + blue;
    }
    return '#'+red+green+blue;
  };

}