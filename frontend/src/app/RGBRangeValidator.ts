import { ValidatorFn, AbstractControl } from '@angular/forms';


export function RGBRangeValidator(): ValidatorFn {
  return (control: AbstractControl): {[key: string]: any} | null => {
    console.log(control);
    let isValid = false;
    if (parseInt(control.value) == parseFloat(control.value) && !isNaN(control.value) && control.value >= 0 && control.value <= 255) {
        isValid = true;
    }
    return isValid ? null: {rgbValidRange : true};
  };
}