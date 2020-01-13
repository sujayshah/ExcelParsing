import { Component, OnInit } from '@angular/core';
import { NgForm, FormControl, FormGroup, Validators, AbstractControl, ValidatorFn, ValidationErrors } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { RGBRangeValidator } from './RGBRangeValidator';
import { MatRadioChange } from '@angular/material/radio';
import { ExcelService } from './excel.service';
// import { ValidateDate } from './validators/date.validator';

export interface Tile {
  color: string;
  text: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  ngOnInit() {
    this.excelService.getColorPalette().subscribe( res => {
      this.tiles = [];
      for(let k in res) {
        let newTile: Tile = {
          text: res[k],
          color: res[k]
        }
        this.tiles.push(newTile);
      }
      this.defaultTiles = Object.assign([], this.tiles);
    }, err => {
      console.log(err);
    })
  }

  ValidateDate(): ValidatorFn {
    return (group: FormGroup): ValidationErrors => {
      const control1 = group.controls['minDate'];
      const control2 = group.controls['maxDate'];
      const mode = group.controls['excelRenderMode']
      let invalid = false
      if(control1.value && control2.value && mode.value == 'program') {
         if( control1.value.format('YYYYMMDD')
          >= control2.value.format('YYYYMMDD')) {
            invalid = true;
          }
      }
      return invalid ? {'invalidDateRange': true} : null;
    };
  }

  excelFileGroup = new FormGroup({
    excelFilePath: new FormControl(null, Validators.required),
    excelRenderMode: new FormControl(null, Validators.required),
    excelFile: new FormControl(null),
    minDate: new FormControl({value: null, disabled: true}),
    maxDate: new FormControl({value: null, disabled: true})
  }, this.ValidateDate())

  clickedAddColor: boolean = false;
  addNewColor: boolean = false;
  validColorRed = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorGreen = new FormControl('', [Validators.required, RGBRangeValidator()]);
  validColorBlue = new FormControl('', [Validators.required, RGBRangeValidator()]);

  tiles: Tile[] = [];
  defaultTiles: Tile[] = [];

  constructor(
    private excelService: ExcelService
  ) {

  }

  focusRenderMode(event : MatRadioChange) {
    this.excelService.getColorPalette(event.value).subscribe( res => {
      this.tiles = [];
      for(let k in res) {
        let newTile: Tile = {
          text: res[k],
          color: res[k]
        }
        this.tiles.push(newTile);
      }
      this.defaultTiles = Object.assign([], this.tiles);
    }, err => {
      console.log(err);
    })
    let minDateControl = this.excelFileGroup.controls['minDate'];
    let maxDateControl = this.excelFileGroup.controls['maxDate'];
    if(event.value == "program") {
      minDateControl.setValidators([Validators.required]);
      minDateControl.enable();
      maxDateControl.setValidators([Validators.required]);
      maxDateControl.enable();
    }
    else {
      minDateControl.clearValidators();
      minDateControl.disable();
      maxDateControl.clearValidators();
      maxDateControl.disable();
    }
    minDateControl.updateValueAndValidity();
    maxDateControl.updateValueAndValidity();
  }

  processFile(fileList : FileList) {
    if(fileList[0]) {
      this.excelFileGroup.get('excelFile').setValue(fileList[0]);
    }
  }

  private prepareSave(form : FormGroup): FormData {
    let input = new FormData();
    if(form.get('excelRenderMode').value == "program") {
      let startDate = form.controls['minDate'].value.format('MM-DD-YYYY');
      let endDate = form.controls['maxDate'].value.format('MM-DD-YYYY');
      input.append('start', startDate);
      input.append('end', endDate);
    }
    input.append('name', form.controls['excelFile'].value);
    this.tiles.forEach(tile => {
      input.append(tile.text, tile.color);
    });
    return input;
  }

  onSubmit(form) {
    const formModel : FormData = this.prepareSave(form);
    if(form.controls['excelRenderMode'].value == "program") {
      this.programValidation(formModel);
    }
    else if(form.controls['excelRenderMode'].value == "resource") {
      this.resourceValidation(formModel);
    }
  }

  programValidation(formData) {
    this.excelService.sendProgramValidation(formData).subscribe( (res) => {
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
  
/////////////////////////////////////////////////

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

  addColor() {
    if(this.validColorRed.valid && this.validColorGreen.valid && this.validColorBlue.valid) {
      let color = this.rgbToHex(this.validColorRed.value, this.validColorGreen.value, this.validColorBlue.value);
      let newTile : Tile = {color: color, text: color.toUpperCase()};
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

}