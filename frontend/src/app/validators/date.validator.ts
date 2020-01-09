import { AbstractControl, ValidatorFn, FormGroup, ValidationErrors } from '@angular/forms';

export function ValidateDate(): ValidatorFn {
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