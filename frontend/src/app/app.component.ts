import { Component } from '@angular/core';
import { NgForm, FormControl, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { RGBRangeValidator } from './RGBRangeValidator';
import { MatRadioChange } from '@angular/material/radio';
import { ExcelService } from './excel.service';
import { MatDatepickerModule } from '@angular/material/datepicker';

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
    excelFilePath: new FormControl(null, Validators.required),
    excelRenderMode: new FormControl(null, Validators.required),
    excelFile: new FormControl('')
  })

  clickedAddColor: boolean = false;
  addNewColor: boolean = false;
  validColorRed = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorGreen = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorBlue = new FormControl('', [Validators.required, RGBRangeValidator()]);

  tiles: Tile[] = [
    {text: '1', color: '#ADD8E6'},
    {text: '2', color: '#90EE90'},
    {text: '3', color: '#FFB6C1'},
    {text: '4', color: '#DDBDF1'},
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
      this.excelFileGroup.get('excelFile').setValue(fileList[0]);
    }
  }

  private prepareSave(): any {
    let input = new FormData();
    input.append('name', this.excelFileGroup.get('excelFile').value);
    this.tiles.forEach(tile => {
      input.append(tile.text, tile.color);
    });
    return input;
  }

  onSubmit(form) {
    const formModel : FormData = this.prepareSave();
    if(form.value.excelRenderMode == "program") {
      this.programValidation(formModel);
    }
    else if(form.value.excelRenderMode == "resource") {
      this.resourceValidation(formModel);
    }
  }

  programValidation(formData) {
    this.excelService.sendProgramValidation(formData).subscribe( (res) => {
      console.log(res);
    },
    err => {
      console.log(err);
    });
  }

  resourceValidation(formData) {
    this.excelService.sendResourceValidation(formData).subscribe( (res : any) => {
      let blob = new Blob([res], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
      let blobFile = new File([blob], "output.xlsx", {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});

      let url = window.URL.createObjectURL(blobFile);
      let anchor = document.createElement("a");
      anchor.download = "output.xlsx"
      anchor.href = url
      anchor.click()
      window.URL.revokeObjectURL(url)
    },
    err => {
    console.log("Error", err);
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