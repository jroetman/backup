import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ColorbarEditorComponent } from './colorbar-editor.component';

describe('ColorbarEditorComponent', () => {
  let component: ColorbarEditorComponent;
  let fixture: ComponentFixture<ColorbarEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ColorbarEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ColorbarEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
