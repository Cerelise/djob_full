import nProgress from 'nprogress'
import { toast as A } from 'vue3-toastify';

export function toast(title, type = 'success', options) {
  A(title, {
    "type": type,
    "dangerouslyHTMLString": true,
    ...options
  })
}

export function resetForm(form) {
  Object.keys(form).forEach((key) => {
    if (typeof form[key] === 'string') form[key] = ""
    else if (typeof form[key] === 'number') form[key] = 0
    else if (typeof form[key] === 'boolean') form[key] = false
    else if (typeof form[key] === 'object') form[key] = {}
    else if (Array.isArray(form[key])) form[key] = []
  })
}

export function showFullLoading() {
  nProgress.start()
}

export function hideFullLoading() {
  nProgress.done()
}