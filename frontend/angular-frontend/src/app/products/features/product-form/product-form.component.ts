import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Product } from '../../../shared/interfaces/product.interface';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './product-form.component.html',
  styleUrl: './product-form.component.scss'
})
export class ProductFormComponent implements OnInit {
  @Input() product?: Product;
  @Output() formSubmit = new EventEmitter<Product>();
  @Output() closeForm = new EventEmitter<void>();
  
  productForm: FormGroup;
  previewImage = '';

  constructor(private fb: FormBuilder) {
    this.productForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      price: [0, [Validators.required, Validators.min(0)]],
      category: ['', Validators.required],
      image: ['', Validators.required],
      rating: this.fb.group({
        rate: [0],
        count: [0]
      })
    });
  }

  ngOnInit(): void {
    if (this.product) {
      this.productForm.patchValue(this.product);
      this.previewImage = this.product.image;
    }
  }

  onImageUrlChange(event: Event) {
    const url = (event.target as HTMLInputElement).value;
    this.previewImage = url;
  }

  showError(fieldName: string): boolean {
    const field = this.productForm.get(fieldName);
    return field?.invalid && (field?.dirty || field?.touched) || false;
  }

  onSubmit() {
    if (this.productForm.valid) {
      const productData = this.productForm.value;
      console.log(this.product ? 'Editando producto:' : 'Creando producto:', productData);
      this.formSubmit.emit(productData);
    }
  }
}
