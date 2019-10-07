# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Storage(object):
    def __init__(self, project_id, *args, **kwargs):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
        'projectId': project_id,
        })
        self.db = firestore.client()
        
    
    def add_labels(self, labels):
        labels = self.db.collections(u'labels')
        labels.document(*labels).create({})
    
    def add_image(self, image_url, labels):
        labels_collection = self.db.collections(u'labels')
        for label in labels:
            label_doc= labels_collection.document(label)
            label_doc.set({'repr_image': image_url, 'images': self.db.ArrayUnion([label])}, merge=True)
            